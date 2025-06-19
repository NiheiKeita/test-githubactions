#!/usr/bin/env python3
"""
GitHubリポジトリのPRコメント一覧を取得するスクリプト
"""

import os
import sys
import json
from datetime import datetime
from github import Github

def get_pr_comments_list(github_token, repo_name):
    """
    リポジトリの全PRのコメント一覧を取得する
    
    Args:
        github_token (str): GitHub APIトークン
        repo_name (str): リポジトリ名 (owner/repo形式)
    
    Returns:
        list: コメント一覧のリスト
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    comments_list = []
    
    # 全PRを取得
    pull_requests = repo.get_pulls(state='all')
    
    for pr in pull_requests:
        print(f"PR #{pr.number}: {pr.title}")
        
        # PRのレビューコメントを取得
        review_comments = pr.get_review_comments()
        for comment in review_comments:
            comments_list.append({
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
                comments_list.append({
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
            comments_list.append({
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
    
    return comments_list

def save_comments_to_json(comments_list, output_file):
    """
    コメント一覧をJSONファイルに保存する
    
    Args:
        comments_list (list): コメント一覧
        output_file (str): 出力ファイル名
    """
    # 集計情報を追加
    summary = {
        'total_comments': len(comments_list),
        'total_prs': len(set(comment['pr_number'] for comment in comments_list)),
        'comment_types': {},
        'users': {},
        'generated_at': datetime.now().isoformat()
    }
    
    # コメントタイプ別集計
    for comment in comments_list:
        comment_type = comment['comment_type']
        summary['comment_types'][comment_type] = summary['comment_types'].get(comment_type, 0) + 1
        
        user = comment['comment_user']
        if user:
            summary['users'][user] = summary['users'].get(user, 0) + 1
    
    # 結果を構造化
    result = {
        'summary': summary,
        'comments': comments_list
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"コメント一覧が保存されました: {output_file}")
    print(f"総コメント数: {len(comments_list)}")
    print(f"総PR数: {summary['total_prs']}")
    print(f"コメントタイプ別:")
    for comment_type, count in summary['comment_types'].items():
        print(f"  - {comment_type}: {count}件")
    print(f"ユーザー別（上位5名）:")
    sorted_users = sorted(summary['users'].items(), key=lambda x: x[1], reverse=True)
    for user, count in sorted_users[:5]:
        print(f"  - {user}: {count}件")

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
    print("PRコメント一覧の取得を開始します...")
    
    try:
        # コメント一覧を取得
        comments_list = get_pr_comments_list(github_token, repo_name)
        
        # JSONファイルに保存
        output_file = 'comments_list.json'
        save_comments_to_json(comments_list, output_file)
        
        print("コメント一覧の取得が完了しました。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラーが発生しても空の結果を保存
        try:
            empty_result = {
                'summary': {
                    'total_comments': 0,
                    'total_prs': 0,
                    'comment_types': {},
                    'users': {},
                    'generated_at': datetime.now().isoformat()
                },
                'comments': []
            }
            with open('comments_list.json', 'w', encoding='utf-8') as f:
                json.dump(empty_result, f, ensure_ascii=False, indent=2)
            print("空のコメント一覧を保存しました。")
        except Exception as json_error:
            print(f"JSONファイルの保存にも失敗しました: {json_error}")
            sys.exit(1)

if __name__ == "__main__":
    main() 