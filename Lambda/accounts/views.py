from wambda.shortcuts import render, redirect
from wambda.authenticate import login, signup, verify, change_password, forgot_password, confirm_forgot_password, MaintenanceOptionError
from .forms import LoginForm, SignupForm, VerifyForm, ChangePasswordForm, ForgotPasswordForm, ResetPasswordForm, DeleteAccountForm

def login_view(master):
    if master.request.method == 'POST':
        form = LoginForm(master.request.get_form_data())
    else:
        form = LoginForm()
    
    context = {'form': form}
    
    # URLパラメータからメッセージを取得
    if master.request.method == 'GET':
        message_type = master.request.query_params.get('message', '')
        
        # メッセージ設定
        if message_type == 'verify_success':
            context['message'] = 'メールアドレスの確認が完了しました'
        elif message_type == 'password_reset_success':
            context['message'] = 'パスワードリセットが完了しました。新しいパスワードでログインしてください。'
    
    if master.request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        try:
            if login(master, username, password):
                return redirect(master, 'home')
            else:
                context['error'] = 'ログインに失敗しました'
                return render(master, 'accounts/login.html', context)
        except MaintenanceOptionError:
            context['error'] = '現在、メンテナンスのためログインできません。しばらくお待ちください。'
            return render(master, 'accounts/login.html', context)
    
    return render(master, 'accounts/login.html', context)

def signup_view(master):
    if master.request.method == 'POST':
        form = SignupForm(master.request.get_form_data())
    else:
        form = SignupForm()
    
    if master.request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            if signup(master, username, email, password):
                # サインアップ成功後は/accounts/verifyにリダイレクトし、ユーザー名をクエリパラメータで渡す
                return redirect(master, 'accounts:verify', query_params={
                    'username': username,
                    'message': 'signup_success'
                })
            else:
                context = {'form': form, 'error': 'サインアップに失敗しました'}
                return render(master, 'accounts/signup.html', context)
        except MaintenanceOptionError:
            context = {'form': form, 'error': '現在、メンテナンスのため新規登録を停止しております。ご迷惑をおかけして申し訳ございません。'}
            return render(master, 'accounts/signup.html', context)
    
    return render(master, 'accounts/signup.html', {'form': form})

def verify_view(master):
    if master.request.method == 'POST':
        form = VerifyForm(master.request.get_form_data())
    else:
        form = VerifyForm()

    context = {'form': form}

    # URLパラメータからユーザー名とメッセージを取得
    if master.request.method == 'GET':
        username = master.request.query_params.get('username', '')
        message_type = master.request.query_params.get('message', '')
        
        if username:
            form.username.data = username
        
        # メッセージ設定
        if message_type == 'signup_success':
            context['message'] = 'サインアップが完了しました。確認コードをメールで送信しました。'
    
    if master.request.method == 'POST' and form.validate():
        username = form.username.data
        code = form.code.data
        if verify(master, username, code):
            # verify成功後は/accounts/loginにリダイレクトしてメッセージを表示
            return redirect(master, 'accounts:login', query_params={
                'message': 'verify_success'
            })
        else:
            context['error'] = '確認に失敗しました'
            return render(master, 'accounts/verify.html', context)
    
    return render(master, 'accounts/verify.html', context)

def logout_view(master):
    from wambda.authenticate import sign_out
    
    try:
        sign_out(master)  # 認証情報クリア + Cookie削除フラグ設定
        master.logger.debug("sign_out completed successfully")
    except Exception as e:
        master.logger.warning(f"Logout warning: {e}")
        # 例外が発生した場合も強制的にCookie削除
        master.request.auth = False
        master.request.username = None
        master.request.clean_cookie = True
        master.logger.debug("Forced cleanup after exception")
    
    # リダイレクト先URLをログ出力
    from wambda.shortcuts import reverse
    home_url = reverse(master, 'home')
    master.logger.debug(f"Redirecting to home URL: {home_url}")
    
    redirect_response = redirect(master, 'home')
    master.logger.debug(f"Redirect response: {redirect_response}")
    
    return redirect_response

def change_password_view(master):
    # Authentication check
    if not master.request.auth:
        return redirect(master, 'accounts:login')
    
    if master.request.method == 'POST':
        form = ChangePasswordForm(master.request.get_form_data())
    else:
        form = ChangePasswordForm()
    
    context = {'form': form}
    
    
    if master.request.method == 'POST' and form.validate():
        current_password = form.current_password.data
        new_password = form.new_password.data
        
        try:
            if change_password(master, current_password, new_password):
                # パスワード変更成功後はアカウント情報ページにリダイレクト
                return redirect(master, 'accounts:profile', query_params={
                    'message': 'password_changed'
                })
            else:
                context['error'] = 'パスワード変更に失敗しました。現在のパスワードを確認してください。'
                return render(master, 'accounts/change_password.html', context)
        except Exception as e:
            master.logger.exception(f"パスワード変更エラー: {e}")
            context['error'] = 'パスワード変更中にエラーが発生しました。'
            return render(master, 'accounts/change_password.html', context)
    
    return render(master, 'accounts/change_password.html', context)

def forgot_password_view(master):
    if master.request.method == 'POST':
        form = ForgotPasswordForm(master.request.get_form_data())
    else:
        form = ForgotPasswordForm()
    
    context = {'form': form}
    
    if master.request.method == 'POST' and form.validate():
        username = form.username.data
        
        try:
            if forgot_password(master, username):
                # パスワードリセット確認コード送信成功後はリセット画面にリダイレクト
                return redirect(master, 'accounts:reset_password', query_params={
                    'username': username,
                    'message': 'code_sent'
                })
            else:
                context['error'] = 'パスワードリセット確認コードの送信に失敗しました。ユーザー名を確認してください。'
                return render(master, 'accounts/forgot_password.html', context)
        except Exception as e:
            master.logger.exception(f"パスワードリセット確認コード送信エラー: {e}")
            context['error'] = 'パスワードリセット確認コード送信中にエラーが発生しました。'
            return render(master, 'accounts/forgot_password.html', context)
    
    return render(master, 'accounts/forgot_password.html', context)

def reset_password_view(master):
    if master.request.method == 'POST':
        form = ResetPasswordForm(master.request.get_form_data())
    else:
        form = ResetPasswordForm()

    context = {'form': form}

    # URLパラメータからユーザー名とメッセージを取得
    if master.request.method == 'GET':
        username = master.request.query_params.get('username', '')
        message_type = master.request.query_params.get('message', '')
        
        if username:
            form.username.data = username
        
        # メッセージ設定
        if message_type == 'code_sent':
            context['message'] = 'パスワードリセット確認コードをメールで送信しました。'
    
    if master.request.method == 'POST' and form.validate():
        username = form.username.data
        confirmation_code = form.confirmation_code.data
        new_password = form.new_password.data
        
        try:
            if confirm_forgot_password(master, username, confirmation_code, new_password):
                # パスワードリセット成功後はログイン画面にリダイレクト
                return redirect(master, 'accounts:login', query_params={
                    'message': 'password_reset_success'
                })
            else:
                context['error'] = 'パスワードリセットに失敗しました。確認コードまたはユーザー名を確認してください。'
                return render(master, 'accounts/reset_password.html', context)
        except Exception as e:
            master.logger.exception(f"パスワードリセットエラー: {e}")
            context['error'] = 'パスワードリセット中にエラーが発生しました。'
            return render(master, 'accounts/reset_password.html', context)
    
    return render(master, 'accounts/reset_password.html', context)

def user_profile_view(master):
    # Authentication check
    if not master.request.auth:
        return redirect(master, 'accounts:login')

    context = {
        'username': master.request.username,
        'user_info': master.request.decode_token if hasattr(master.request, 'decode_token') else {}
    }

    # URLパラメータからメッセージを取得
    message_type = master.request.query_params.get('message', '')

    # メッセージ設定
    if message_type == 'password_changed':
        context['message'] = 'パスワードが正常に変更されました'

    return render(master, 'accounts/user_profile.html', context)

def delete_account_view(master):
    # Authentication check
    if not master.request.auth:
        return redirect(master, 'accounts:login')

    if master.request.method == 'POST':
        form = DeleteAccountForm(master.request.get_form_data())
    else:
        form = DeleteAccountForm()

    context = {'form': form}

    if master.request.method == 'POST' and form.validate():
        current_password = form.current_password.data
        username = master.request.username

        try:
            # パスワード認証を行う
            if login(master, username, current_password):
                # 実際のアカウント削除処理（Cognitoから削除）
                import boto3
                from botocore.exceptions import ClientError
                from wambda.authenticate import get_cognito_settings

                client = boto3.client('cognito-idp', region_name=master.settings.REGION)
                cognito_settings = get_cognito_settings(master)

                try:
                    # ユーザーを削除
                    client.admin_delete_user(
                        UserPoolId=cognito_settings['USER_POOL_ID'],
                        Username=username
                    )

                    master.logger.info(f"アカウント削除成功: ユーザー {username}")

                    # サインアウトしてホームページにリダイレクト
                    from wambda.authenticate import sign_out
                    try:
                        sign_out(master)
                    except Exception as e:
                        master.logger.warning(f"Delete account logout warning: {e}")
                        # 例外が発生した場合も強制的にCookie削除
                        master.request.auth = False
                        master.request.username = None
                        master.request.clean_cookie = True

                    return redirect(master, 'home', query_params={
                        'message': 'account_deleted'
                    })

                except ClientError as e:
                    error_code = e.response['Error']['Code']
                    master.logger.error(f"アカウント削除エラー: {error_code}")
                    context['error'] = 'アカウント削除中にエラーが発生しました。'
                    return render(master, 'accounts/delete_account.html', context)

            else:
                context['error'] = 'パスワードが正しくありません。'
                return render(master, 'accounts/delete_account.html', context)

        except Exception as e:
            master.logger.exception(f"アカウント削除エラー: {e}")
            context['error'] = 'アカウント削除中にエラーが発生しました。'
            return render(master, 'accounts/delete_account.html', context)

    return render(master, 'accounts/delete_account.html', context)