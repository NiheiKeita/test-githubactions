#!/usr/bin/env python3
"""
GitHubリポジトリのPRコメント数を集計するスクリプト
"""

import os
import sys
import json
from github import Github

def count_pr_comments(github_token, repo_name):
    """
    リポジトリの全PRのコメント数を集計する
    
    Args:
        github_token (str): GitHub APIトークン
        repo_name (str): リポジトリ名 (owner/repo形式)
    
    Returns:
        dict: 集計結果
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # 集計用の変数
    total_prs = 0
    total_comments = 0
    review_comments = 0
    reviews = 0
    issue_comments = 0
    prs_with_comments = 0
    prs_without_comments = 0
    
    # 全PRを取得
    pull_requests = repo.get_pulls(state='all')
    
    for pr in pull_requests:
        total_prs += 1
        pr_comment_count = 0
        
        print(f"PR #{pr.number}: {pr.title}")
        
        # PRのレビューコメントを取得
        pr_review_comments = list(pr.get_review_comments())
        review_comments += len(pr_review_comments)
        pr_comment_count += len(pr_review_comments)
        
        # PRのレビューを取得
        pr_reviews = list(pr.get_reviews())
        for review in pr_reviews:
            if review.body:  # レビューコメントがある場合のみ
                reviews += 1
                pr_comment_count += 1
        
        # PRのissueコメントを取得
        pr_issue_comments = list(pr.get_issue_comments())
        issue_comments += len(pr_issue_comments)
        pr_comment_count += len(pr_issue_comments)
        
        # PRの総コメント数を更新
        total_comments += pr_comment_count
        
        # コメントの有無を記録
        if pr_comment_count > 0:
            prs_with_comments += 1
        else:
            prs_without_comments += 1
    
    # 平均コメント数を計算
    avg_comments_per_pr = round(total_comments / total_prs, 2) if total_prs > 0 else 0
    
    return {
        'total_prs': total_prs,
        'total_comments': total_comments,
        'review_comments': review_comments,
        'reviews': reviews,
        'issue_comments': issue_comments,
        'avg_comments_per_pr': avg_comments_per_pr,
        'prs_with_comments': prs_with_comments,
        'prs_without_comments': prs_without_comments
    }

def save_counts_to_json(counts_data, output_file):
    """
    集計結果をJSONファイルに保存する
    
    Args:
        counts_data (dict): 集計結果
        output_file (str): 出力ファイル名
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(counts_data, f, ensure_ascii=False, indent=2)
    
    print(f"集計結果が保存されました: {output_file}")
    print(f"総PR数: {counts_data['total_prs']}件")
    print(f"総コメント数: {counts_data['total_comments']}件")
    print(f"レビューコメント: {counts_data['review_comments']}件")
    print(f"レビュー: {counts_data['reviews']}件")
    print(f"Issueコメント: {counts_data['issue_comments']}件")
    print(f"平均コメント数/PR: {counts_data['avg_comments_per_pr']}件")

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
    print("PRコメント数の集計を開始します...")
    
    try:
        # コメント数を集計
        counts_data = count_pr_comments(github_token, repo_name)
        
        # JSONファイルに保存
        output_file = 'comment_counts.json'
        save_counts_to_json(counts_data, output_file)
        
        print("集計が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラーが発生しても空の結果を保存
        try:
            empty_counts = {
                'total_prs': 0,
                'total_comments': 0,
                'review_comments': 0,
                'reviews': 0,
                'issue_comments': 0,
                'avg_comments_per_pr': 0,
                'prs_with_comments': 0,
                'prs_without_comments': 0
            }
            with open('comment_counts.json', 'w', encoding='utf-8') as f:
                json.dump(empty_counts, f, ensure_ascii=False, indent=2)
            print("空の集計結果を保存しました。")
        except Exception as json_error:
            print(f"JSONファイルの保存にも失敗しました: {json_error}")
            sys.exit(1)

if __name__ == "__main__":
    main() 