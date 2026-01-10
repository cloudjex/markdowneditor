# MarkdownEditor

## CICD Status
[![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

## Summary
markdown管理アプリ用のPublicRepository。  
Serverless Architectureを使用した、シンプルなFrontend/Backend構成。  
Serverlessを採用し、安価に構築/運用。OSS Applicationとして公開中。

App: [cloudjex.com](https://www.cloudjex.com)

## System Overview
以下のFramework/技術要素を使用

| Framework/技術要素 | 言語       | 用途     |
| ------------------ | ---------- | -------- |
| FastApi            | Python     | Backend  |
| React              | TypeScript | Frontend |
| GithubActions      | yaml       | CICD     |
| Terraform          | tf         | CICD     |

<br>

以下のサービスを使用

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

NoSQL(ドキュメント指向DB)を使用し、Itemは単一テーブルに格納  

主キー: `PK`  
ソートキー: `SK`

### user item
| key       | type   | desctiption            | description        |
| --------- | ------ | ---------------------- | ------------------ |
| PK        | str    | value: `EMAIL#{email}` | PartitionKey       |
| SK        | str    | value: `PROFILE`       | SortKey            |
| password  | str    | hashed pw              |                    |
| options   | object | other settings         |                    |
| ├ enabled | bool   | active/inactive        |                    |
| └ otp     | str    | otp                    | only inactive user |

### tree item
| key       | type   | desctiption            | description  |
| --------- | ------ | ---------------------- | ------------ |
| PK        | str    | value: `EMAIL#{email}` | PartitionKey |
| SK        | str    | value: `TREE`          | SortKey      |
| node_tree | object | tree content           |              |

### node item
| key  | type | desctiption             | description  |
| ---- | ---- | ----------------------- | ------------ |
| PK   | str  | value: `EMAIL#{email}`  | PartitionKey |
| SK   | str  | value: `NODE#{node id}` | SortKey      |
| text | str  | text                    |              |
