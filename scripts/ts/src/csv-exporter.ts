import { createObjectCsvWriter } from 'csv-writer';
import { PRComment } from './types';

export class CSVExporter {
  private csvWriter: any;

  constructor(outputPath: string) {
    this.csvWriter = createObjectCsvWriter({
      path: outputPath,
      header: [
        { id: 'pr_number', title: 'PR番号' },
        { id: 'pr_title', title: 'PRタイトル' },
        { id: 'pr_state', title: 'PR状態' },
        { id: 'pr_created_at', title: 'PR作成日時' },
        { id: 'pr_merged_at', title: 'PRマージ日時' },
        { id: 'pr_author', title: 'PR作成者' },
        { id: 'comment_type', title: 'コメントタイプ' },
        { id: 'comment_id', title: 'コメントID' },
        { id: 'comment_body', title: 'コメント内容' },
        { id: 'comment_created_at', title: 'コメント作成日時' },
        { id: 'comment_updated_at', title: 'コメント更新日時' },
        { id: 'comment_user', title: 'コメント投稿者' },
        { id: 'comment_path', title: 'コメント対象ファイルパス' },
        { id: 'comment_line', title: 'コメント対象行番号' },
        { id: 'comment_side', title: 'コメント対象サイド' },
        { id: 'comment_start_line', title: 'コメント開始行番号' },
        { id: 'comment_start_side', title: 'コメント開始サイド' },
      ],
      encoding: 'utf8',
    });
  }

  async exportComments(comments: PRComment[]): Promise<void> {
    try {
      await this.csvWriter.writeRecords(comments);
      console.log(`CSVファイルが生成されました: ${comments.length}件のコメント`);
    } catch (error) {
      console.error('CSVファイルの出力中にエラーが発生しました:', error);
      throw error;
    }
  }
} 