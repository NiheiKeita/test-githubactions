import { GitHubClient } from './github-client';
import { CSVExporter } from './csv-exporter';
import { PRComment } from './types';
import { format } from 'date-fns';

async function getAllPRComments(token: string, repository: string): Promise<PRComment[]> {
  const client = new GitHubClient(token, repository);
  const comments: PRComment[] = [];

  try {
    console.log('PRの取得を開始します...');
    const pullRequests = await client.getAllPullRequests();
    console.log(`${pullRequests.length}件のPRが見つかりました。`);

    for (const pr of pullRequests) {
      console.log(`PR #${pr.number}: ${pr.title}`);

      // PRのレビューコメントを取得
      try {
        const reviewComments = await client.getReviewComments(pr.number);
        for (const comment of reviewComments) {
          comments.push({
            pr_number: pr.number,
            pr_title: pr.title,
            pr_state: pr.state,
            pr_created_at: pr.created_at,
            pr_merged_at: pr.merged_at || '',
            pr_author: pr.user?.login || '',
            comment_type: 'review_comment' as const,
            comment_id: comment.id,
            comment_body: comment.body || '',
            comment_created_at: comment.created_at,
            comment_updated_at: comment.updated_at,
            comment_user: comment.user?.login || '',
            comment_path: comment.path || '',
            comment_line: comment.line || null,
            comment_side: comment.side || '',
            comment_start_line: comment.start_line || null,
            comment_start_side: comment.start_side || '',
          });
        }
      } catch (error) {
        console.error(`PR #${pr.number}のレビューコメント取得でエラー:`, error);
      }

      // PRのレビューを取得
      try {
        const reviews = await client.getReviews(pr.number);
        for (const review of reviews) {
          if (review.body) {
            comments.push({
              pr_number: pr.number,
              pr_title: pr.title,
              pr_state: pr.state,
              pr_created_at: pr.created_at,
              pr_merged_at: pr.merged_at || '',
              pr_author: pr.user?.login || '',
              comment_type: 'review' as const,
              comment_id: review.id,
              comment_body: review.body,
              comment_created_at: review.submitted_at || '',
              comment_updated_at: review.submitted_at || '',
              comment_user: review.user?.login || '',
              comment_path: '',
              comment_line: null,
              comment_side: '',
              comment_start_line: null,
              comment_start_side: '',
            });
          }
        }
      } catch (error) {
        console.error(`PR #${pr.number}のレビュー取得でエラー:`, error);
      }

      // PRのissueコメントを取得
      try {
        const issueComments = await client.getIssueComments(pr.number);
        for (const comment of issueComments) {
          comments.push({
            pr_number: pr.number,
            pr_title: pr.title,
            pr_state: pr.state,
            pr_created_at: pr.created_at,
            pr_merged_at: pr.merged_at || '',
            pr_author: pr.user?.login || '',
            comment_type: 'issue_comment' as const,
            comment_id: comment.id,
            comment_body: comment.body || '',
            comment_created_at: comment.created_at,
            comment_updated_at: comment.updated_at,
            comment_user: comment.user?.login || '',
            comment_path: '',
            comment_line: null,
            comment_side: '',
            comment_start_line: null,
            comment_start_side: '',
          });
        }
      } catch (error) {
        console.error(`PR #${pr.number}のissueコメント取得でエラー:`, error);
      }
    }
  } catch (error) {
    console.error('PRの取得中にエラーが発生しました:', error);
    throw error;
  }

  return comments;
}

async function main() {
  const token = process.env.GITHUB_TOKEN;
  const repository = process.env.GITHUB_REPOSITORY;

  if (!token) {
    console.error('GITHUB_TOKEN環境変数が設定されていません。');
    process.exit(1);
  }

  if (!repository) {
    console.error('GITHUB_REPOSITORY環境変数が設定されていません。');
    process.exit(1);
  }

  console.log(`リポジトリ: ${repository}`);
  console.log('PRコメントのCSV出力を開始します...');

  try {
    // コメントデータを取得
    const comments = await getAllPRComments(token, repository);

    if (comments.length === 0) {
      console.log('コメントデータが見つかりませんでした。');
      return;
    }

    // CSVファイルに出力
    const outputFile = 'pr_comments_export.csv';
    const exporter = new CSVExporter(outputFile);
    await exporter.exportComments(comments);

    // 統計情報を表示
    const uniquePRs = new Set(comments.map(c => c.pr_number));
    const commentTypes = comments.reduce((acc, comment) => {
      acc[comment.comment_type] = (acc[comment.comment_type] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);

    const users = comments.reduce((acc, comment) => {
      if (comment.comment_user) {
        acc[comment.comment_user] = (acc[comment.comment_user] || 0) + 1;
      }
      return acc;
    }, {} as Record<string, number>);

    console.log('\n=== 統計情報 ===');
    console.log(`総コメント数: ${comments.length}`);
    console.log(`総PR数: ${uniquePRs.size}`);
    console.log('コメントタイプ別:');
    Object.entries(commentTypes).forEach(([type, count]) => {
      console.log(`  - ${type}: ${count}件`);
    });
    console.log('ユーザー別（上位10名）:');
    Object.entries(users)
      .sort(([, a], [, b]) => b - a)
      .slice(0, 10)
      .forEach(([user, count]) => {
        console.log(`  - ${user}: ${count}件`);
      });

    console.log('CSV出力が完了しました。');

  } catch (error) {
    console.error('エラーが発生しました:', error);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
} 