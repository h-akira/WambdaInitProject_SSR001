#!/usr/bin/env python3
"""
WAMBDA Sample Project - Sample Data Generator

このスクリプトは、WAMBDA Sample Projectにサンプルデータを投入するためのツールです。
開発・テスト環境で使用することを想定しています。

使用方法:
    python bin/sample_data.py --username [ユーザー名]

例:
    python bin/sample_data.py --username testuser
"""

import sys
import os
import argparse
import uuid
from datetime import datetime, timezone

# プロジェクトルートをPythonパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Lambda'))

import boto3
from wambda.handler import Master

def put_data(item, table_name=None):
    """DynamoDBにデータを保存"""
    if table_name is None:
        table_name = os.environ.get('DYNAMODB_TABLE', 'wambda-table-ssr001')
    
    dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
    table = dynamodb.Table(table_name)
    table.put_item(Item=item)

def create_sample_categories(username):
    """サンプルカテゴリーを作成"""
    categories = [
        {'name': '仕事', 'color': 'blue'},
        {'name': 'プライベート', 'color': 'green'},
        {'name': '学習', 'color': 'purple'},
        {'name': '買い物', 'color': 'yellow'},
        {'name': '健康', 'color': 'red'},
    ]
    
    created_categories = []
    now = datetime.now(timezone.utc)
    
    for cat_data in categories:
        category_id = str(uuid.uuid4())
        category = {
            'pk': f"user#{username}#category",
            'sk': category_id,
            'name': cat_data['name'],
            'color': cat_data['color'],
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        
        put_data(category)
        created_categories.append(category)
        print(f"カテゴリーを作成: {cat_data['name']}")
    
    return created_categories

def create_sample_todos(username, categories):
    """サンプルTodoを作成"""
    todos = [
        {
            'title': 'プロジェクトの企画書作成',
            'description': '新プロジェクトの企画書をドラフトして、関係者にレビューを依頼する',
            'priority': 'high',
            'completed': False,
            'category': '仕事'
        },
        {
            'title': 'WAMBDAフレームワークの学習',
            'description': 'ドキュメントを読んで基本機能を理解する',
            'priority': 'medium',
            'completed': True,
            'category': '学習'
        },
        {
            'title': '食材の買い出し',
            'description': '週末の食事の準備のため、スーパーで食材を購入',
            'priority': 'medium',
            'completed': False,
            'category': '買い物'
        },
        {
            'title': 'ジム通い',
            'description': '週3回のジム通いを継続する',
            'priority': 'low',
            'completed': True,
            'category': '健康'
        },
        {
            'title': '友人との食事会',
            'description': '来週の土曜日に友人と食事の約束',
            'priority': 'low',
            'completed': False,
            'category': 'プライベート'
        },
        {
            'title': 'AWSの請求書確認',
            'description': '今月の請求額をチェックして、コスト最適化を検討',
            'priority': 'high',
            'completed': False,
            'category': '仕事'
        },
        {
            'title': 'Python新機能の調査',
            'description': '最新バージョンの新機能について調査・検証',
            'priority': 'medium',
            'completed': False,
            'category': '学習'
        },
        {
            'title': '定期検診の予約',
            'description': '年に一度の健康診断の予約を取る',
            'priority': 'high',
            'completed': True,
            'category': '健康'
        }
    ]
    
    # カテゴリー名からIDへのマッピングを作成
    category_map = {cat['name']: cat['sk'] for cat in categories}
    
    now = datetime.now(timezone.utc)
    
    for todo_data in todos:
        todo_id = str(uuid.uuid4())
        
        todo = {
            'pk': f"user#{username}#todo",
            'sk': todo_id,
            'title': todo_data['title'],
            'description': todo_data['description'],
            'priority': todo_data['priority'],
            'completed': todo_data['completed'],
            'category_id': category_map.get(todo_data['category'], ''),
            'created_at': now.isoformat(),
            'updated_at': now.isoformat()
        }
        
        put_data(todo)
        status = "完了" if todo_data['completed'] else "未完了"
        print(f"Todoを作成: {todo_data['title']} ({status})")

def main():
    parser = argparse.ArgumentParser(description='WAMBDA Sample Project サンプルデータ投入ツール')
    parser.add_argument('--username', required=True, help='サンプルデータを作成するユーザー名')
    parser.add_argument('--clean', action='store_true', help='既存データを削除してから作成')
    
    args = parser.parse_args()
    
    # モック環境のMasterインスタンスを作成
    # 実際の環境では適切な設定が必要
    event = {}
    context = {}
    master = Master(event, context)
    
    print(f"ユーザー '{args.username}' のサンプルデータを作成します...")
    
    try:
        # サンプルカテゴリーを作成
        print("\n=== カテゴリー作成 ===")
        categories = create_sample_categories(args.username)
        
        # サンプルTodoを作成
        print("\n=== Todo作成 ===")
        create_sample_todos(args.username, categories)
        
        print(f"\n✅ サンプルデータの作成が完了しました！")
        print(f"カテゴリー: {len(categories)}個")
        print(f"Todo: 8個")
        print(f"\nブラウザで https://your-app-url/{args.username}/dashboard にアクセスして確認してください。")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()