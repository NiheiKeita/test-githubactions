#!/usr/bin/env python3
"""
GitHubリポジトリのPRコメントをCSVファイルとして出力するスクリプト
"""

import os
import sys
import csv
from datetime import datetime
from github import Github
import pandas as pd

def get_all_pr_comments(github_token, repo_name):
    """
    リポジトリの全PRのコメントを取得する
    
    Args:
        github_token (str): GitHub APIトークン
        repo_name (str): リポジトリ名 (owner/repo形式)
    
    Returns:
        list: コメントデータのリスト
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    comments_data = []
    
    # 全PRを取得
    pull_requests = repo.get_pulls(state='all')
    
    for pr in pull_requests:
        print(f"PR #{pr.number}: {pr.title}")
        
        # PRのレビューコメントを取得
        review_comments = pr.get_review_comments()
        for comment in review_comments:
            comments_data.append({
                'pr_number': pr.number,
                'pr_title': pr.title,
                'pr_state': pr.state,
                'pr_created_at': pr.created_at.isoformat(),
                'pr_merged_at': pr.merged_at.isoformat() if pr.merged_at else '',
                'comment_type': 'review_comment',
                'comment_id': comment.id,
                'comment_body': comment.body,
                'comment_created_at': comment.created_at.isoformat(),
                'comment_updated_at': comment.updated_at.isoformat(),
                'comment_user': comment.user.login if comment.user else '',
                'comment_path': comment.path,
                'comment_line': comment.line,
                'comment_side': comment.side,
                'comment_start_line': comment.start_line,
                'comment_start_side': comment.start_side
            })
        
        # PRのレビューを取得
        reviews = pr.get_reviews()
        for review in reviews:
            if review.body:  # レビューコメントがある場合のみ
                comments_data.append({
                    'pr_number': pr.number,
                    'pr_title': pr.title,
                    'pr_state': pr.state,
                    'pr_created_at': pr.created_at.isoformat(),
                    'pr_merged_at': pr.merged_at.isoformat() if pr.merged_at else '',
                    'comment_type': 'review',
                    'comment_id': review.id,
                    'comment_body': review.body,
                    'comment_created_at': review.submitted_at.isoformat(),
                    'comment_updated_at': review.submitted_at.isoformat(),
                    'comment_user': review.user.login if review.user else '',
                    'comment_path': '',
                    'comment_line': '',
                    'comment_side': '',
                    'comment_start_line': '',
                    'comment_start_side': ''
                })
        
        # PRのissueコメントを取得
        issue_comments = pr.get_issue_comments()
        for comment in issue_comments:
            comments_data.append({
                'pr_number': pr.number,
                'pr_title': pr.title,
                'pr_state': pr.state,
                'pr_created_at': pr.created_at.isoformat(),
                'pr_merged_at': pr.merged_at.isoformat() if pr.merged_at else '',
                'comment_type': 'issue_comment',
                'comment_id': comment.id,
                'comment_body': comment.body,
                'comment_created_at': comment.created_at.isoformat(),
                'comment_updated_at': comment.updated_at.isoformat(),
                'comment_user': comment.user.login if comment.user else '',
                'comment_path': '',
                'comment_line': '',
                'comment_side': '',
                'comment_start_line': '',
                'comment_start_side': ''
            })
    
    return comments_data

def export_to_csv(comments_data, output_file):
    """
    コメントデータをCSVファイルに出力する
    
    Args:
        comments_data (list): コメントデータのリスト
        output_file (str): 出力ファイル名
    """
    if not comments_data:
        print("コメントデータが見つかりませんでした。空のCSVファイルを生成します。")
        # 空のCSVファイルをヘッダー付きで生成
        df = pd.DataFrame(columns=[
            'pr_number', 'pr_title', 'pr_state', 'pr_created_at', 'pr_merged_at',
            'comment_type', 'comment_id', 'comment_body', 'comment_created_at',
            'comment_updated_at', 'comment_user', 'comment_path', 'comment_line',
            'comment_side', 'comment_start_line', 'comment_start_side'
        ])
    else:
        # DataFrameに変換
        df = pd.DataFrame(comments_data)
    
    # CSVに出力（UTF-8 BOM付きで日本語対応）
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"CSVファイルが生成されました: {output_file}")
    print(f"総コメント数: {len(comments_data)}")
    print(f"PR数: {df['pr_number'].nunique() if not df.empty else 0}")
    
    # 統計情報を表示
    if not df.empty:
        print("\n=== 統計情報 ===")
        print(f"コメントタイプ別件数:")
        print(df['comment_type'].value_counts())
        print(f"\nユーザー別コメント数（上位10名）:")
        print(df['comment_user'].value_counts().head(10))

def main():
    """メイン関数"""
    # GitHubトークンを取得
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("エラー: GITHUB_TOKEN環境変数が設定されていません。")
        sys.exit(1)
    
    # リポジトリ名を取得
    repo_name = os.environ.get('GITHUB_REPOSITORY')
    if not repo_name:
        print("エラー: GITHUB_REPOSITORY環境変数が設定されていません。")
        sys.exit(1)
    
    print(f"リポジトリ: {repo_name}")
    print("PRコメントのCSV出力を開始します...")
    
    try:
        # コメントデータを取得
        comments_data = get_all_pr_comments(github_token, repo_name)
        
        # CSVファイルに出力
        output_file = 'pr_comments_export.csv'
        export_to_csv(comments_data, output_file)
        
        print("CSV出力が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラーが発生しても空のCSVファイルを生成
        try:
            empty_df = pd.DataFrame(columns=[
                'pr_number', 'pr_title', 'pr_state', 'pr_created_at', 'pr_merged_at',
                'comment_type', 'comment_id', 'comment_body', 'comment_created_at',
                'comment_updated_at', 'comment_user', 'comment_path', 'comment_line',
                'comment_side', 'comment_start_line', 'comment_start_side'
            ])
            empty_df.to_csv('pr_comments_export.csv', index=False, encoding='utf-8-sig')
            print("空のCSVファイルを生成しました。")
        except Exception as csv_error:
            print(f"CSVファイルの生成にも失敗しました: {csv_error}")
            sys.exit(1)

if __name__ == "__main__":
    main() 