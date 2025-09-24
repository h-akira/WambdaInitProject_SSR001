import boto3

def set_data():
  """SSM Parameter Storeのモックデータを設定"""
  ssm = boto3.client('ssm')
  
  # 必要なパラメータを設定
  parameters = [
    {
      'Name': '/Cognito/user_pool_id',
      'Value': 'ap-northeast-1_testuserpool',
      'Type': 'String'
    },
    {
      'Name': '/Cognito/client_id',
      'Value': 'testclientid',
      'Type': 'String'
    },
    {
      'Name': '/Cognito/client_secret',
      'Value': 'testclientsecret',
      'Type': 'String'
    }
  ]
  
  for param in parameters:
    try:
      ssm.put_parameter(
        Name=param['Name'],
        Value=param['Value'],
        Type=param['Type'],
        Overwrite=True
      )
    except Exception as e:
      print(f"SSM parameter setting error: {e}")