# MarkdownEditor

## CICD Status
[![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

## Summary
markdown管理アプリ用のPublicRepositoryです。  
Serverless Architectureを使用した、シンプルなFrontend/Backend構成となります。  
Serverlessを採用することで、非常に安価に構築/運用しています。  
OSS Applicationとして公開しておりますので、気軽にご利用ください。

App: [cloudjex.com](https://www.cloudjex.com)

## System Overview
本Repositoryでは以下のFramework/技術要素を使用しています。

| Framework/技術要素 | 言語       | 用途     |
| ------------------ | ---------- | -------- |
| FastApi            | Python     | Backend  |
| React              | TypeScript | Frontend |
| GithubActions      | yaml       | CICD     |
| Terraform          | tf         | CICD     |

<br>

本Repositoryでは以下のサービスを使用しています。

| サービス       | 用途               |
| -------------- | ------------------ |
| AWS Lambda     | FastApi実行環境    |
| AWS ApiGateway | FastApi配信        |
| AWS DynamoDB   | DB                 |
| AWS S3         | React格納/配信     |
| AWS CloudFront | React配信          |
| Resend         | SMTP               |
| お名前.com     | DNS, Custom Domain |

## Table Design

### users table
| key       | type   | desctiption     | description        |
| --------- | ------ | --------------- | ------------------ |
| email     | str    | email           | Partition Key      |
| password  | str    | hashed pw       |                    |
| options   | object | other settings  |                    |
| ├ enabled | bool   | active/inactive |                    |
| └ otp     | str    | otp             | only inactive user |

### trees table
| key   | type   | desctiption  | description   |
| ----- | ------ | ------------ | ------------- |
| email | str    | email        | Partition Key |
| tree  | object | tree content |               |

### nodes table
| key   | type | desctiption | description   |
| ----- | ---- | ----------- | ------------- |
| email | str  | email       | Partition Key |
| id    | str  | node id     | Sort Key      |
| text  | str  | text        |               |
