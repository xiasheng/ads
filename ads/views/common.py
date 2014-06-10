
from django.http import HttpResponse
from random import Random
import json


#ERROR_CODE
E_SYSTEM = 10001
E_AUTH = 10002
E_PARAM = 10003
E_NOT_SUPPORT = 10004

class MyException(Exception):
    def __init__(self, info):      
        Exception.__init__(self)  
        self.info = info

class MyParamError(MyException):
    pass

def RandomStr(rlen=64):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(rlen):
        str+=chars[random.randint(0, length)]
    return str

def SuccessResponse(content):
    content['success'] = True
    return HttpResponse(json.dumps(content),  content_type="application/json")

def ErrorResponse(err_code, info=''):
    content = {} 
    content['success'] = False

    if err_code == E_SYSTEM:
        content['message'] = 'system error'
    elif err_code == E_AUTH:
        content['message'] = 'auth eror'
    elif err_code == E_PARAM:
        content['message'] = 'param illegal'
    elif err_code == E_NOT_SUPPORT:
        content['message'] = 'not support'
 
    if info:
        content['message'] = info

    return HttpResponse(json.dumps(content),  content_type="application/json")
