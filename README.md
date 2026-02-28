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
| key       | type   | value           | description                       |
| --------- | ------ | --------------- | --------------------------------- |
| PK        | str    | `EMAIL#{email}` | PartitionKey                      |
| SK        | str    | `USER`          | SortKey                           |
| password  | str    |                 | hashed by bcrypt                  |
| groups    | array  |                 | array of group ids                |
| options   | object |                 |                                   |
| ├ enabled | bool   |                 |                                   |
| └ otp     | str    |                 | only inactive user has this value |

### user group
| key         | type  | value                 | description           |
| ----------- | ----- | --------------------- | --------------------- |
| PK          | str   | `GROUP_ID#{group_id}` | PartitionKey          |
| SK          | str   | `USER_GROUP`          | SortKey               |
| group_name  | str   |                       |                       |
| users       | array |                       | array of user objects |
| ├ [i].email | str   |                       | email                 |
| └ [i].role  | str   |                       | `admin` or `member`   |

### node item
| key          | type  | value                 | description  |
| ------------ | ----- | --------------------- | ------------ |
| PK           | str   | `GROUP_ID#{group_id}` | PartitionKey |
| SK           | str   | `NODE#{node_id}`      | SortKey      |
| label        | str   |                       |              |
| text         | str   |                       |              |
| children_ids | array | children node ids     |              |

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
