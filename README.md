# MarkdownEditor

## CICD Status
[![CICD Workflow](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml/badge.svg)](https://github.com/cloudjex/markdowneditor/actions/workflows/cicd.yaml)

## Summary
- markdown管理アプリ用のPublicRepository
- Frontend/Backend共にServerless Architectureを使用
- App URL: https://www.cloudjex.com
- OpenAPI: https://api.cloudjex.com/docs

## System Overview
以下のFramework/技術要素を使用

| Framework/技術要素 | 言語       | 用途     |
| ------------------ | ---------- | -------- |
| FastApi            | Python     | Backend  |
| React              | TypeScript | Frontend |
| GithubActions      | yaml       | CICD     |
| Terraform          | tf         | CICD     |

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

- 主キー: `PK`  
- ソートキー: `SK`

### user item
| key         | type   | desctiption            | description        |
| ----------- | ------ | ---------------------- | ------------------ |
| PK          | str    | value: `EMAIL#{email}` | PartitionKey       |
| SK          | str    | value: `USER`          | SortKey            |
| password    | str    | hashed pw              |                    |
| user_groups | array  | user groups            |                    |
| options     | object | other settings         |                    |
| ├ enabled   | bool   | active/inactive        |                    |
| └ otp       | str    | otp                    | only inactive user |


### user group
| key   | type  | desctiption                      | description  |
| ----- | ----- | -------------------------------- | ------------ |
| PK    | str   | value: `GROUP_NAME#{user_group}` | PartitionKey |
| SK    | str   | value: `USER_GROUP`              | SortKey      |
| users | array | users                            |              |

### tree info item
| key        | type   | desctiption                      | description           |
| ---------- | ------ | -------------------------------- | --------------------- |
| PK         | str    | value: `GROUP_NAME#{user_group}` | PartitionKey          |
| SK         | str    | value: `USER_GROUP`              | SortKey               |
| tree       | object | tree content                     |                       |
| ├ node_id  | str    | node id                          |                       |
| ├ label    | str    | node label                       |                       |
| └ children | object | node children                    | have tree recursively |

### node item
| key  | type | desctiption                      | description  |
| ---- | ---- | -------------------------------- | ------------ |
| PK   | str  | value: `GROUP_NAME#{user_group}` | PartitionKey |
| SK   | str  | value: `NODE#{node_id}`          | SortKey      |
| text | str  | text                             |              |

## For Developer
FastAPI in local
```sh
cd ./fastapi
pip install -r requirements.txt
uvicorn app:app --reload
```

React in local
```sh
cd ./react
npm i
npm run dev
```
