# DynamoDB テーブル設計書

## 概要

このドキュメントはWAMBDA TODO アプリケーションのDynamoDBテーブル設計について説明します。

## テーブル構成

### 基本情報
- **テーブル名**: `wambda-table-ssr001` (環境変数 `DYNAMODB_TABLE` で設定)
- **リージョン**: `ap-northeast-1`
- **課金モード**: `PAY_PER_REQUEST`

### キースキーマ
- **パーティションキー (PK)**: `pk` (String)
- **ソートキー (SK)**: `sk` (String)

## データ設計パターン

### 単一テーブル設計
このアプリケーションではDynamoDBのベストプラクティスである単一テーブル設計を採用しています。

### エンティティ構造

#### 1. ユーザー情報
```
PK: users
SK: {username}
```

**属性:**
- `username`: ユーザー名
- `email`: メールアドレス

**例:**
```json
{
  "pk": "users",
  "sk": "testuser", 
  "username": "testuser",
  "email": "test@example.com"
}
```

#### 2. Todo
```
PK: user#{username}
SK: todo#{todo_id}
```

**属性:**
- `id`: TodoのUUID (後方互換性のため)
- `entity_type`: "todo"
- `title`: Todoのタイトル
- `description`: Todoの説明
- `priority`: 優先度 ("high", "medium", "low")
- `completed`: 完了状態 (Boolean)
- `category_id`: 関連するカテゴリのID
- `created_at`: 作成日時 (ISO 8601形式)
- `updated_at`: 更新日時 (ISO 8601形式)

**例:**
```json
{
  "pk": "user#testuser",
  "sk": "todo#550e8400-e29b-41d4-a716-446655440000",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "entity_type": "todo",
  "title": "プロジェクトの企画書作成",
  "description": "新プロジェクトの企画書をドラフトして、関係者にレビューを依頼する",
  "priority": "high",
  "completed": false,
  "category_id": "category001",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

#### 3. Category
```
PK: user#{username}
SK: category#{category_id}
```

**属性:**
- `id`: CategoryのUUID (後方互換性のため)
- `entity_type`: "category"
- `name`: カテゴリ名
- `color`: カテゴリの色 (Bulmaクラス名)
- `created_at`: 作成日時 (ISO 8601形式)
- `updated_at`: 更新日時 (ISO 8601形式)

**色の選択肢:**
- `primary`: Blue (Primary)
- `info`: Light Blue (Info)
- `success`: Green (Success)
- `warning`: Yellow (Warning)  
- `danger`: Red (Danger)
- `link`: Dark Blue (Link)
- `light`: Light Gray
- `dark`: Dark Gray

**例:**
```json
{
  "pk": "user#testuser",
  "sk": "category#category001",
  "id": "category001",
  "entity_type": "category", 
  "name": "仕事",
  "color": "primary",
  "created_at": "2024-01-01T00:00:00.000Z",
  "updated_at": "2024-01-01T00:00:00.000Z"
}
```

## アクセスパターン

### 1. 特定ユーザーのすべてのTodoを取得
```python
response = table.query(
    KeyConditionExpression=Key('pk').eq('user#testuser') & 
                          Key('sk').begins_with('todo#')
)
```

### 2. 特定ユーザーのすべてのCategoryを取得
```python
response = table.query(
    KeyConditionExpression=Key('pk').eq('user#testuser') & 
                          Key('sk').begins_with('category#')
)
```

### 3. 特定ユーザーのすべてのデータを取得
```python
response = table.query(
    KeyConditionExpression=Key('pk').eq('user#testuser')
)
```

### 4. 特定のTodoを取得
```python
response = table.get_item(
    Key={
        'pk': 'user#testuser',
        'sk': 'todo#550e8400-e29b-41d4-a716-446655440000'
    }
)
```

### 5. 特定のCategoryを取得
```python
response = table.get_item(
    Key={
        'pk': 'user#testuser', 
        'sk': 'category#category001'
    }
)
```

## 設計の利点

### 1. 効率的なクエリ
- ユーザーごとのデータを効率的に取得
- エンティティタイプによる前方一致フィルタリング
- 1回のクエリで複数エンティティを取得可能

### 2. 拡張性
- 新しいエンティティタイプを簡単に追加可能
- ユーザー数の増加に対してスケーラブル

### 3. DynamoDBベストプラクティス準拠
- 単一テーブル設計パターン
- ホットパーティション問題の回避
- コスト効率的なデータ配置

### 4. 後方互換性
- `id` フィールドによる既存コードとの互換性維持
- `entity_type` フィールドによる明示的なタイプ識別

## ヘルパー関数

アプリケーションでは以下のヘルパー関数を提供しています：

### データ取得
- `get_user_data_by_type(username, entity_type)`: 特定エンティティタイプのデータを取得
- `get_user_all_data(username)`: ユーザーの全データを取得
- `get_data_by_pk_sk(pk, sk)`: PKとSKで単一アイテムを取得

### データ作成
- `create_todo_item(username, todo_data)`: 新設計でTodoアイテムを作成
- `create_category_item(username, category_data)`: 新設計でCategoryアイテムを作成

### データ操作
- `put_data(item)`: アイテムを保存
- `delete_data_by_pk_sk(pk, sk)`: PKとSKでアイテムを削除