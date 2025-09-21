from wambda.shortcuts import render

def home(master):
  context = {}

  # URLパラメータからメッセージを取得
  query_params = master.request.query_params
  message_type = query_params.get('message', '')

  # メッセージ設定
  if message_type == 'account_deleted':
    context['message'] = 'アカウントが削除されました。ご利用いただき、ありがとうございました。'
    context['message_type'] = 'success'

  return render(master, 'home.html', context)

def custom_not_found_view(master):
  """Custom 404 view using not_found.html template"""
  context = {}
  return render(master, 'not_found.html', context, code=404)
