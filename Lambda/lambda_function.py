import sys
import os
from wambda.handler import Master
from moto import mock_aws

def lambda_handler(event, context):
  sys.path.append(os.path.dirname(__file__))
  master = Master(event, context)
  master.logger.info(f"path: {master.request.path}")
  master.logger.debug(f"LOG_LEVEL: {master.settings.LOG_LEVEL}")
  try:
    if master.settings.USE_MOCK:
      return use_mock(master)
    else:
      return main(master)
  except Exception as e:
    if master.request.path == "/favicon.ico":
      master.logger.warning("favicon.ico not found")
    else:
      master.logger.exception(e)
    from wambda.shortcuts import error_render
    import traceback
    return error_render(master, traceback.format_exc())

def main(master):
  from wambda.authenticate import set_auth_by_cookie, add_set_cookie_to_header
  set_auth_by_cookie(master)
  view, kwargs = master.get_view(master.request.path)
  response = view(master, **kwargs)
  
  # Cookie処理前のログ
  master.logger.debug(f"Before cookie processing - set_cookie: {master.request.set_cookie}")
  master.logger.debug(f"Before cookie processing - clean_cookie: {master.request.clean_cookie}")

  add_set_cookie_to_header(master, response)

  # Cookie処理後のログ
  master.logger.debug(f"Response structure: {response}")
  if "multiValueHeaders" in response and "Set-Cookie" in response["multiValueHeaders"]:
    master.logger.debug(f"Cookie headers: {response['multiValueHeaders']['Set-Cookie']}")
  else:
    master.logger.debug("No cookie headers set")
  
  return response

@mock_aws
def use_mock(master):
  from mock.dynamodb import set_data as set_dynamodb_data
  from mock.ssm import set_data as set_ssm_data
  from wambda.authenticate import set_auth_by_cookie, add_set_cookie_to_header
  set_dynamodb_data()
  set_ssm_data()
  set_auth_by_cookie(master)
  view, kwargs = master.get_view(master.request.path)
  response = view(master, **kwargs)
  
  # Cookie処理前のログ
  master.logger.debug(f"Before cookie processing - set_cookie: {master.request.set_cookie}")
  master.logger.debug(f"Before cookie processing - clean_cookie: {master.request.clean_cookie}")
  
  add_set_cookie_to_header(master, response)
  
  # Cookie処理後のログ
  master.logger.debug(f"Response structure: {response}")
  if "multiValueHeaders" in response and "Set-Cookie" in response["multiValueHeaders"]:
    master.logger.debug(f"Cookie headers: {response['multiValueHeaders']['Set-Cookie']}")
  else:
    master.logger.debug("No cookie headers set")
  
  return response

if __name__ == "__main__":
  from wambda.debug import main_debug_handler
  main_debug_handler(lambda_handler)
