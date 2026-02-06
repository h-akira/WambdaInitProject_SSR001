import os
MAPPING_PATH = os.environ.get('WAMBDA_MAPPING_PATH', "")  # API Gatewayをそのまま使う場合はステージ名、独自ドメインを使う場合は空文字列
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),"../"))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_URL = "/static"  # 先頭の/はあってもなくても同じ扱
TIMEZONE = "Asia/Tokyo"

# ログレベル設定 (INFO, DEBUG, WARNING, ERROR)
LOG_LEVEL = os.environ.get('WAMBDA_LOG_LEVEL', 'INFO')  # 環境変数から取得、未定義時は"INFO"

# 認証周りの設定 - SSMパラメータ名の定義
COGNITO_SSM_PARAMS = {
    'USER_POOL_ID': '/WambdaInit/Cognito/user_pool_id',
    'CLIENT_ID': '/WambdaInit/Cognito/client_id',
    'CLIENT_SECRET': '/WambdaInit/Cognito/client_secret'
}
REGION = "ap-northeast-1"
# 
# 下記は/またはhttp(s)://で始まる場合はそのまま、それ以外の場合はRouter.name2pathで生成したパスにリダイレクト
LOGIN_URL = "accounts:login"  # ログインページのURL
SIGNUP_URL = "accounts:signup"  # サインアップページのURL
VERIFY_URL = "accounts:verify"  # メールアドレス確認ページのURL
LOGOUT_URL = "accounts:logout"  # ログアウトページのURL
# 認証周りの設定ここまで

# テスト用の設定
DEBUG = os.environ.get("WAMBDA_DEBUG", "False").lower() == "true" if os.environ.get("WAMBDA_DEBUG") else True
USE_MOCK = os.environ.get("WAMBDA_USE_MOCK", "False").lower() == "true" if os.environ.get("WAMBDA_USE_MOCK") else False
NO_AUTH = os.environ.get("WAMBDA_NO_AUTH", "False").lower() == "true" if os.environ.get("WAMBDA_NO_AUTH") else False
DENY_SIGNUP = os.environ.get("WAMBDA_DENY_SIGNUP", "False").lower() == "true" if os.environ.get("WAMBDA_DENY_SIGNUP") else False
DENY_LOGIN = os.environ.get("WAMBDA_DENY_LOGIN", "False").lower() == "true" if os.environ.get("WAMBDA_DENY_LOGIN") else False

# Custom 404 view
from project.views import custom_not_found_view
URL_NOT_MATCHED_VIEW = custom_not_found_view
