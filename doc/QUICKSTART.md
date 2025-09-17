# WAMBDA Sample Project - クイックスタートガイド

このガイドでは、WAMBDA Sample Projectを使って開発を始める方法を説明します。

## 前提条件

- Python 3.9 以上
- AWS CLI (設定済み)
- SAM CLI
- Git

## セットアップ手順

### 1. プロジェクトのクローン/コピー

```bash
# 新しいプロジェクトディレクトリを作成
mkdir my-hads-project
cd my-hads-project

# HadsInitProject_SSR001の内容をコピー
cp -r /path/to/HadsInitProject_SSR001/* .
```

### 2. プロジェクト名の変更

プロジェクト固有の設定を更新します：

```bash
# README.md のタイトルを変更
sed -i '' 's/WAMBDA Sample Project/My WAMBDA Project/g' README.md

# template.yaml のプロジェクト名を更新
# エディターで template.yaml を開いて以下を変更：
# - Transform, Description
# - 各リソース名のプレフィックス
```

### 3. 依存関係のインストール

```bash
# Lambda 層の依存関係をインストール
pip install -r Lambda/requirements.txt -t Lambda/
```

### 4. ローカル開発環境の準備

```bash
# 環境変数の設定
cp local_env.json.sample local_env.json
# local_env.json を編集して適切な値を設定

# デバッグスクリプトの実行権限を付与
chmod +x debug.sh
```

### 5. ローカルでのテスト

```bash
# ローカルサーバーを起動
./debug.sh

# ブラウザで http://localhost:8000 にアクセス
```

### 6. AWS環境へのデプロイ

```bash
# SAM ビルド
sam build

# 初回デプロイ (ガイド付き)
sam deploy --guided

# 設定が保存された後は以下で再デプロイ可能
sam deploy
```

## 機能の追加方法

### 新しいアプリケーションの追加

1. **モジュールの作成**
```bash
mkdir Lambda/myapp
touch Lambda/myapp/__init__.py
touch Lambda/myapp/urls.py
touch Lambda/myapp/views.py
touch Lambda/myapp/forms.py
```

2. **ビューの実装**
```python
# Lambda/myapp/views.py
from hads.shortcuts import render, redirect
from hads.authenticate import login_required

@login_required
def index(master, username):
    return render(master, 'myapp/index.html', {'username': username})
```

3. **URLパターンの追加**
```python
# Lambda/myapp/urls.py
from hads.urls import Path
from .views import index

urlpatterns = [
    Path("{username}/myapp", index, name="index"),
]
```

4. **メインURLに追加**
```python
# Lambda/project/urls.py に追加
Router("", "myapp.urls", name="myapp"),
```

5. **テンプレートの作成**
```bash
mkdir Lambda/templates/myapp
# Lambda/templates/myapp/index.html を作成
```

### データベース設計のガイドライン

WAMBDAはDynamoDBを使用しており、単一テーブル設計パターンを採用しています。詳細は `doc/table.md` を参照してください。

```python
# 新設計パターン: ユーザー固有データ
{
    'pk': 'user#{username}',            # パーティションキー
    'sk': '{entity_type}#{entity_id}',  # ソートキー
    'id': 'entity_id',                  # 後方互換性のため
    'entity_type': 'todo',              # エンティティタイプ
    # その他の属性...
}

# 例: Todoデータ
{
    'pk': 'user#alice',
    'sk': 'todo#550e8400-e29b-41d4-a716-446655440000',
    'id': '550e8400-e29b-41d4-a716-446655440000',
    'entity_type': 'todo',
    'title': 'Sample Todo',
    'description': 'Todo description',
    'priority': 'medium',
    'completed': False,
    'category_id': 'category001',
    'created_at': '2024-01-01T00:00:00.000Z',
    'updated_at': '2024-01-01T00:00:00.000Z'
}

# 例: Categoryデータ
{
    'pk': 'user#alice',
    'sk': 'category#category001',
    'id': 'category001',
    'entity_type': 'category',
    'name': '仕事',
    'color': 'primary',
    'created_at': '2024-01-01T00:00:00.000Z',
    'updated_at': '2024-01-01T00:00:00.000Z'
}
```

**推奨ヘルパー関数:**
```python
# 特定エンティティタイプのデータを取得
todos = get_user_data_by_type(username, 'todo')
categories = get_user_data_by_type(username, 'category')

# 新しいアイテムを作成
todo_item = create_todo_item(username, todo_data)
category_item = create_category_item(username, category_data)
```

## トラブルシューティング

### よくある問題

**1. デプロイ時の権限エラー**
```bash
# IAMロールに適切な権限があることを確認
aws iam list-attached-role-policies --role-name SAM-execution-role
```

**2. DynamoDBアクセスエラー**
```python
# テーブル名が正しく設定されているか確認
# Lambda/project/settings.py の TABLE_NAME を確認
```

**3. 静的ファイルが表示されない**
```bash
# S3バケットの設定を確認
aws s3 ls s3://your-static-bucket/
```

## 開発のベストプラクティス

### 1. コード構成
- 機能ごとにアプリケーションを分割
- ビジネスロジックはviews.pyに集約
- データベースアクセスは適切に抽象化

### 2. テンプレート
- base.htmlを継承して一貫性を保つ
- ブロックを適切に使い分ける
- Bulmaクラスを活用してレスポンシブ対応

### 3. セキュリティ
- `@login_required`デコレータを適切に使用
- ユーザーデータのアクセス制御を厳密に実装
- CSRFトークンを忘れずに含める

### 4. パフォーマンス
- DynamoDBのクエリを効率化
- 静的ファイルはS3+CloudFrontで配信
- Lambda の cold start を考慮した設計

## 次のステップ

1. **認証機能の拡張**: プロフィール編集、パスワード変更など
2. **API機能の追加**: REST API エンドポイントの実装
3. **外部サービス連携**: SES（メール）、SNS（通知）などの活用
4. **監視機能**: CloudWatch によるログ・メトリクス監視
5. **CI/CD環境**: GitHub Actions などを使用した自動デプロイ

## リソース

- [テーブル設計書](table.md) - このプロジェクトのDynamoDB設計詳細
- [WAMBDA フレームワーク ドキュメント](https://github.com/h-akira/hads)
- [AWS SAM 開発者ガイド](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/)
- [DynamoDB 設計ガイド](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Bulma CSS ドキュメント](https://bulma.io/documentation/)

## サポート

質問や問題がある場合は、以下のリソースを活用してください：

- WAMBDA フレームワーク: [GitHub Issues](https://github.com/h-akira/hads/issues)
- AWS サポート: AWS Developer Forums
- コミュニティ: Stack Overflow (aws-lambda, dynamodb タグ)