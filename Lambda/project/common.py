import random

def gen_code(length):
  """ランダムな文字列を生成"""
  allow="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  return ''.join(random.choice(allow) for i in range(length))
