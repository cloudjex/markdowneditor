# Copilot Instructions

このファイルには、GitHub Copilot が このリポジトリで効果的に支援するためのガイドラインが含まれています。

## プロジェクト概要

- FastAPIとReactを使用したモノリポジトリ構成のMarkdownエディタプロジェクト
- バックエンド
  - API Gatewayを介してHTTPリクエストを処理
  - Lambda上でFastAPIを実行
- フロントエンド
  - AWS S3をホスティングに使用
  - CloudFrontをCDNとして利用
- データストレージ
  - AWS DynamoDBを使用
- メール送信
  - Resendを利用
- DNS/カスタムドメイン
  - お名前.comを使用

詳細: `markdowneditor/README.md`

## コーディング規約

- 共通
  - GitHub Issues, Pull Requestは日本語で記載する
  - コード内のコメントは英語で記載する
  - コミットメッセージは英語で記載する
  - KISSの原則に従う
  - ファイルの末尾には改行を入れる
  - コード内の定数は大文字で記載する
- Python
  - スタイル
    - `PEP8`, `Black Formatter`に準拠する
    - その他のコーディングスタイルは一般的なPython記法に準拠する
    - 型ヒントを積極的に使用する
  - 実装
    - OpenAPI仕様書と実装仕様が一致することを確認する
    - Pytestを用いてテストを実施する(目標カバレッジ90%以上)
    - エラーハンドリング
      - FastAPIの標準例外処理に従い、適切なHTTPステータスコードを返す
- TypeScript
  - スタイル
    - `react/eslint.config.js`に準拠する
    - その他のコーディングスタイルは一般的なReact記法に準拠する
    - Any型の使用は避け、必要な場合は適切な型定義を行う

## Project管理
- タスク管理はGitHub Projectsの`markdowneditor pj`を使用
- タスクはissueとして作成し、Backlogカラムに配置

## ブランチ戦略
- `main`ブランチは常に安定した状態を保ち、リリース可能なコードのみを含む
- ブランチはissueごとに作成し、命名規則は`feature/issue#<issue-number>`とする（例: `feature/issue#123`）
- プルリクエストは、コードレビューを経て`main`ブランチにマージされる前に、少なくとも1人のレビュアーによって承認される必要がある
- マージ前に、すべてのテストが成功することを確認する
- マージ後は、関連するissueをクローズする
