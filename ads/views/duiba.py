
from django.http import HttpResponse
import json, hashlib
from ads.models.models import User, Duiba
from urllib import unquote

class SignException(Exception):
    pass

class UserException(Exception):
    pass

class AreadyExistException(Exception):
    pass


def checkSign(request):
    ret = {}

    params = request.GET.copy()
    sign = params['sign']
    del params['sign']
    params['appSecret'] = 'test'
    params_sorted = sorted(params.iteritems(),key=lambda e:e[0],reverse=False)

    s = ''
    for p in params_sorted:
        s += p[1]

    if sign == hashlib.md5(s).hexdigest():
        return
        
    raise SignException


def QueryCredit(request):
    ret = {}
    try:
        appKey = request.GET.get('appKey')
        timestamp = request.GET.get('timestamp')
        uid = request.GET.get('uid')

        checkSign(request)
        
        user = User.objects.get(user_id=int(uid))

        data = {}
        data['credits'] = user.total_points
        data['phone'] = ''
        data['alipay'] = ''
        data['qq'] = ''

        ret['status'] = 'ok'
        ret['data'] = data
        ret['message'] = 'ok'
    except SignException:
        ret['status'] = 'fail'
        ret['message'] = 'error'
        ret['errormessage'] = 'sign error'
    except:
        ret['status'] = 'fail'
        ret['message'] = 'error'
        ret['errormessage'] = 'error error'

    return HttpResponse(json.dumps(ret),  content_type="application/json")



def ConsumeCredit(request):
    ret = {}
    try:
        appKey = request.GET.get('appKey')
        timestamp = request.GET.get('timestamp')
        uid = request.GET.get('uid')
        credits = int( request.GET.get('credits') )
        description = unquote( request.GET.get('description') )
        orderNum = request.GET.get('orderNum')
        type = request.GET.get('type')        
        facePrice = int( request.GET.get('facePrice') )
        actualPrice = int( request.GET.get('actualPrice') )
        alipay = request.GET.get('alipay')
        phone = request.GET.get('phone')
        qq = request.GET.get('qq')
        waitAudit = request.GET.get('waitAudit')                       
 
        checkSign(request)
                     
        user = User.objects.get(user_id=int(uid))
        
        if user.total_points < credits:
            raise UserException;
        
        if len( Duiba.objects.filter(orderNum=orderNum) ) > 0:
            raise AreadyExistException;

        Duiba.objects.create(appKey=appKey, timestamp=timestamp, uid=uid, credits=credits, 
        description=description, orderNum=orderNum, dtype=type, facePrice=facePrice, actualPrice=actualPrice,
        alipay=alipay, phone=phone, qq=qq, waitAudit=orderNum, status='processing')
 
        user.total_points -= credits
        user.save()
       
        data = {}
        data['credits'] = user.total_points
        data['bizId'] = orderNum
                
        ret['status'] = 'ok'
        ret['data'] = data
        ret['message'] = 'ok'
        ret['errormessage'] = ''

    except SignException:
        ret['status'] = 'fail'
        ret['message'] = 'error'
        ret['errormessage'] = 'sign error'             
    except AreadyExistException:
        ret['status'] = 'fail'
        ret['message'] = 'duplicated orderNum'
        ret['errormessage'] = 'duplicated orderNum' 
    except:
        ret['status'] = 'fail'
        ret['message'] = 'error'
        ret['errormessage'] = 'error'
        
    return HttpResponse(json.dumps(ret),  content_type="application/json")


def ResultCredit(request):
    ret = {}
    try:
        appKey = request.GET.get('appKey')
        timestamp = request.GET.get('timestamp')
        uid = request.GET.get('uid')
        bizId = request.GET.get('bizId')
        success = request.GET.get('success')
        errorMessage = request.GET.get('errorMessage', '')
        
        checkSign(request)

        user = User.objects.get(user_id=int(uid))
                    
        assert len(Duiba.objects.filter(orderNum=bizId) ) == 1
        
        duiba = Duiba.objects.get(orderNum=bizId)
        if success == 'true':
            duiba.status = 'success'
            duiba.save()
        else:
            duiba.status = 'fail'
            duiba.save()  
            
            user.total_points -= credits
            user.save()
    except:
        pass

    return HttpResponse('ok')


