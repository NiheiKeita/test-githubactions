# GitHub Actions PR Comments CSV Exporter

このリポジトリは、GitHub Actionsを使用してプルリクエスト作成時にリポジトリの全PRのコメントを取得し、CSVファイルとして出力するワークフローを提供します。

## 機能

- プルリクエスト作成時に自動実行
- リポジトリの全PR（オープン・クローズ・マージ済み）のコメントを取得
- 以下のコメントタイプを収集：
  - レビューコメント（コードレビュー）
  - レビュー（PRレビュー）
  - Issueコメント（PRのコメント）
- CSVファイルとして出力
- GitHub Actionsのアーティファクトとして保存
- PRにコメントで結果を通知

## 出力されるCSVの列

| 列名 | 説明 |
|------|------|
| pr_number | PR番号 |
| pr_title | PRタイトル |
| pr_state | PRの状態（open/closed） |
| pr_created_at | PR作成日時 |
| pr_merged_at | PRマージ日時 |
| comment_type | コメントタイプ（review_comment/review/issue_comment） |
| comment_id | コメントID |
| comment_body | コメント内容 |
| comment_created_at | コメント作成日時 |
| comment_updated_at | コメント更新日時 |
| comment_user | コメント投稿者 |
| comment_path | コメント対象ファイルパス |
| comment_line | コメント対象行番号 |
| comment_side | コメント対象サイド |
| comment_start_line | コメント開始行番号 |
| comment_start_side | コメント開始サイド |

## 使用方法

1. このワークフローは、プルリクエストが作成・更新・再オープンされた際に自動的に実行されます
2. 実行結果は以下の方法で確認できます：
   - GitHub ActionsのアーティファクトとしてCSVファイルをダウンロード
   - PRのコメントで結果概要を確認

## 必要な権限

このワークフローを実行するには、以下の権限が必要です：

- `contents: read` - リポジトリの内容を読み取り
- `pull-requests: read` - プルリクエストを読み取り
- `issues: write` - PRにコメントを投稿

## 注意事項

- GitHub APIのレート制限に注意してください
- 大量のPRがあるリポジトリでは実行時間が長くなる可能性があります
- コメント内容には機密情報が含まれる可能性があるため、CSVファイルの取り扱いに注意してください

## カスタマイズ

`scripts/export_pr_comments.py`を編集することで、以下のカスタマイズが可能です：

- 取得するコメントタイプの変更
- 出力する列の追加・削除
- フィルタリング条件の追加
- 出力形式の変更

