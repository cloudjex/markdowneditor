# Copilot Instructions

このファイルには、GitHub Copilot が このリポジトリで効果的に支援するためのガイドラインが含まれています。

## プロジェクト概要

FastAPIとReactを使用したモノリポジトリ構成のMarkdownエディタプロジェクトです。
バックエンドはAWS Lambda上でFastAPIを実行し、フロントエンドはAWS S3とCloudFrontを使用してReactアプリケーションを配信します。
データストレージにはAWS DynamoDBを使用し、メール送信にはResendを利用しています。
DNSとカスタムドメインはお名前.comで管理しています。

詳細: `markdowneditor/README.md`

## コーディング規約

- 共通
  - Github Issues, Pull Requestは日本語で記載してください
  - コード内のコメントは英語で記載してください
  - コミットメッセージは英語で記載してください
  - KISSの原則に従ってください
  - ファイルの末尾には改行を入れてください
- Python
  - スタイル
    - `PEP8`, `Black Formatter`に準拠してください
    - その他のコーディングスタイルは一般的なPython記法に準拠してください
    - コード内の定数は大文字で記載してください
  - 実装
    - Pytestを用いてテストを実施してください
    - OpenAPI仕様書と実装仕様が一致することを確認してください
- TypeScript
  - スタイル
    - `react/eslint.config.js`に準拠してください
    - その他のコーディングスタイルは一般的なReact記法に準拠してください
    - コード内の定数は大文字で記載してください

## Project管理
- タスク管理はGitHub Projectsの`markdowneditor pj`を使用してください
- タスクはissueとして作成し、Backlogカラムに配置してください

## ブランチ戦略
- `main`ブランチは常に安定した状態を保ち、リリース可能なコードのみを含むようにしてください。
- ブランチはissueごとに作成し、命名規則は`feature/issue#<issue-number>`としてください（例: `feature/issue#123`）。
- プルリクエストは、コードレビューを経て`main`ブランチにマージされる前に、少なくとも1人のレビュアーによって承認される必要があります。
- マージ前に、すべてのテストが成功することを確認してください。
- マージ後は、関連するissueをクローズしてください。
