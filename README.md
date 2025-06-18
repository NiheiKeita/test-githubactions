# GitHub Actions PR Comments Tools

このリポジトリは、GitHub Actionsを使用してプルリクエスト作成時にリポジトリの全PRのコメントを分析する複数のワークフローを提供します。

## 機能

### 1. PR Comments Counter
- プルリクエスト作成時に自動実行
- リポジトリの全PR（オープン・クローズ・マージ済み）のコメント数を集計
- 集計結果をログに表示

### 2. PR Comments List (JSON)
- プルリクエスト作成時に自動実行
- リポジトリの全PRのコメント一覧をJSON形式で取得
- 詳細なコメント情報と統計情報を提供
- GitHub Actionsのアーティファクトとして保存

### 3. PR Comments CSV Export
- プルリクエスト作成時に自動実行
- リポジトリの全PRのコメントをCSVファイルとして出力
- GitHub Actionsのアーティファクトとして保存
- **CSVファイルをダウンロードしてExcel等で分析可能**

## CSVファイルの使い方

### ダウンロード方法

1. **PRを作成または修正**
2. **GitHubのリポジトリページにアクセス**
3. **Actionsタブをクリック**
4. **"PR Comments CSV Export"ワークフローの実行を確認**
5. **実行完了後、アーティファクトセクションで「pr-comments-csv」をクリック**
6. **「pr_comments_export.csv」をダウンロード**

### CSVファイルの列構成

| 列名 | 説明 |
|------|------|
| pr_number | PR番号 |
| pr_title | PRタイトル |
| pr_state | PRの状態（open/closed） |
| pr_created_at | PR作成日時 |
| pr_merged_at | PRマージ日時 |
| pr_author | PR作成者 |
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

### 分析例

#### Excelでの分析
1. **CSVファイルをExcelで開く**
2. **データタブ → テーブルとして変換**
3. **フィルター機能で特定の条件で絞り込み**
   - 特定のPR作成者のコメント
   - 特定のコメントタイプ
   - 特定の期間のコメント

#### ピボットテーブルでの分析
1. **挿入タブ → ピボットテーブル**
2. **以下のような分析が可能：**
   - ユーザー別コメント数
   - PR別コメント数
   - コメントタイプ別集計
   - 月別コメント数推移

#### データ分析の例
```sql
-- ユーザー別コメント数ランキング
SELECT comment_user, COUNT(*) as comment_count
FROM pr_comments
GROUP BY comment_user
ORDER BY comment_count DESC;

-- PR別コメント数
SELECT pr_number, pr_title, COUNT(*) as comment_count
FROM pr_comments
GROUP BY pr_number, pr_title
ORDER BY comment_count DESC;

-- コメントタイプ別集計
SELECT comment_type, COUNT(*) as count
FROM pr_comments
GROUP BY comment_type;
```

## 集計される情報

### コメントタイプ
- **レビューコメント**：コードレビュー時の行単位コメント
- **レビュー**：PRレビュー時のコメント
- **Issueコメント**：PRのコメント欄のコメント

### 統計情報
- 総PR数
- 総コメント数
- コメントタイプ別件数
- ユーザー別コメント数
- 平均コメント数/PR
- コメントがあるPR数
- コメントがないPR数

## 使用方法

1. このワークフローは、プルリクエストが作成・更新・再オープンされた際に自動的に実行されます
2. 実行結果は以下の方法で確認できます：
   - **Actionsタブ**：ワークフローの実行状況とログ
   - **アーティファクト**：CSVファイルとJSONファイルのダウンロード
   - **PRコメント**：集計結果の概要（一部ワークフロー）

## 必要な権限

このワークフローを実行するには、以下の権限が必要です：

- `contents: read` - リポジトリの内容を読み取り
- `pull-requests: read` - プルリクエストを読み取り

## 注意事項

- GitHub APIのレート制限に注意してください
- 大量のPRがあるリポジトリでは実行時間が長くなる可能性があります
- フォークされたリポジトリからのPRでも動作します
- CSVファイルはUTF-8 BOM付きで出力されるため、日本語も正しく表示されます
- アーティファクトは30日間保存されます

## カスタマイズ

各スクリプトを編集することで、以下のカスタマイズが可能です：

- 取得するコメントタイプの変更
- 出力する列の追加・削除
- フィルタリング条件の追加
- 出力形式の変更

