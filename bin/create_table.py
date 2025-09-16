#!/usr/bin/env python3
"""
WAMBDA Sample Project - DynamoDB Table Creator

このスクリプトは、WAMBDA Sample ProjectのDynamoDBテーブルを作成するためのツールです。

使用方法:
    python bin/create_table.py --table-name [テーブル名] --profile [AWSプロファイル]

例:
    python bin/create_table.py --table-name wambda-table-ssr001
    python bin/create_table.py --table-name wambda-table-ssr001 --profile development
"""

import argparse
import boto3
from botocore.exceptions import ClientError

def create_table(table_name, profile=None, region='ap-northeast-1'):
    """DynamoDBテーブルを作成"""
    
    # セッションの作成
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
    
    dynamodb = session.resource('dynamodb', region_name=region)
    
    try:
        # テーブルが既に存在するかチェック
        existing_table = dynamodb.Table(table_name)
        existing_table.load()
        print(f"テーブル '{table_name}' は既に存在します。")
        return existing_table
    except ClientError as e:
        if e.response['Error']['Code'] != 'ResourceNotFoundException':
            raise e
    
    # テーブルを作成
    print(f"テーブル '{table_name}' を作成中...")
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'pk',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'sk',
                'AttributeType': 'S'
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    
    # テーブルの作成完了を待機
    print("テーブル作成の完了を待っています...")
    table.wait_until_exists()
    
    print(f"✅ テーブル '{table_name}' の作成が完了しました！")
    return table

def main():
    parser = argparse.ArgumentParser(description='WAMBDA Sample Project DynamoDBテーブル作成ツール')
    parser.add_argument('--table-name', 
                        default='wambda-table-ssr001',
                        help='作成するテーブル名 (デフォルト: wambda-table-ssr001)')
    parser.add_argument('--profile', 
                        help='使用するAWSプロファイル (未指定の場合はデフォルト)')
    parser.add_argument('--region',
                        default='ap-northeast-1',
                        help='AWSリージョン (デフォルト: ap-northeast-1)')
    
    args = parser.parse_args()
    
    try:
        table = create_table(args.table_name, args.profile, args.region)
        
        print(f"\n📊 テーブル情報:")
        print(f"   テーブル名: {table.table_name}")
        print(f"   リージョン: {args.region}")
        print(f"   ARN: {table.table_arn}")
        
        print(f"\n💡 次のステップ:")
        print(f"   1. 環境変数を設定: export DYNAMODB_TABLE={args.table_name}")
        print(f"   2. サンプルデータを投入: python bin/sample_data.py --username testuser")
        
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        return 1

if __name__ == '__main__':
    exit(main())