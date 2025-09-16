import boto3
import os

def set_data():
    """DynamoDBのモックデータを設定"""
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table_name = os.environ.get('DYNAMODB_TABLE', 'wambda-table-ssr001')

    # テーブル作成（存在しない場合のみ）
    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'pk', 'KeyType': 'HASH'},
                {'AttributeName': 'sk', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'pk', 'AttributeType': 'S'},
                {'AttributeName': 'sk', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        
        print(f"Created table {table_name}")
        # テーブルが作成されるまで待機
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print(f"Table {table_name} already exists")
        table = dynamodb.Table(table_name)

    # サンプルデータ
    items = [
        # テストユーザー
        {
            'pk': 'users',
            'sk': 'testuser',
            'username': 'testuser',
            'email': 'test@example.com'
        },
        # サンプルカテゴリー
        {
            'pk': 'user#testuser#category',
            'sk': 'category001',
            'name': '仕事',
            'color': 'blue',
            'created_at': '2024-01-01T00:00:00.000Z',
            'updated_at': '2024-01-01T00:00:00.000Z'
        },
        {
            'pk': 'user#testuser#category',
            'sk': 'category002', 
            'name': 'プライベート',
            'color': 'green',
            'created_at': '2024-01-01T00:00:00.000Z',
            'updated_at': '2024-01-01T00:00:00.000Z'
        },
        {
            'pk': 'user#testuser#category',
            'sk': 'category003',
            'name': '学習',
            'color': 'purple',
            'created_at': '2024-01-01T00:00:00.000Z',
            'updated_at': '2024-01-01T00:00:00.000Z'
        },
        # サンプルTodo
        {
            'pk': 'user#testuser#todo',
            'sk': 'todo001',
            'title': 'プロジェクトの企画書作成',
            'description': '新プロジェクトの企画書をドラフトして、関係者にレビューを依頼する',
            'priority': 'high',
            'completed': False,
            'category_id': 'category001',
            'created_at': '2024-01-01T00:00:00.000Z',
            'updated_at': '2024-01-01T00:00:00.000Z'
        },
        {
            'pk': 'user#testuser#todo',
            'sk': 'todo002',
            'title': 'WAMBDAフレームワークの学習',
            'description': 'ドキュメントを読んで基本機能を理解する',
            'priority': 'medium',
            'completed': True,
            'category_id': 'category003',
            'created_at': '2024-01-02T00:00:00.000Z',
            'updated_at': '2024-01-02T00:00:00.000Z'
        },
        {
            'pk': 'user#testuser#todo',
            'sk': 'todo003',
            'title': '友人との食事会',
            'description': '来週の土曜日に友人と食事の約束',
            'priority': 'low',
            'completed': False,
            'category_id': 'category002',
            'created_at': '2024-01-03T00:00:00.000Z',
            'updated_at': '2024-01-03T00:00:00.000Z'
        },
        {
            'pk': 'user#testuser#todo',
            'sk': 'todo004',
            'title': 'AWS請求書の確認',
            'description': '今月の請求額をチェックして、コスト最適化を検討',
            'priority': 'high',
            'completed': False,
            'category_id': 'category001',
            'created_at': '2024-01-04T00:00:00.000Z',
            'updated_at': '2024-01-04T00:00:00.000Z'
        }
    ]
    
    for item in items:
        table.put_item(Item=item)
    print(f"Inserted {len(items)} items into {table_name}")