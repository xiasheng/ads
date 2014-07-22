

from ads.views.common import *
from ads.models.models import User
from django.conf import settings
from django.core.cache import cache
import random, hashlib

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def generateUserId():
    id = 0
    while True:
        id = random.randint(100000, 200000)
        if User.objects.filter(user_id=id).count() > 0:
            continue
        else:
            return id
    return id


def checkParam(mac, dev_id, token):
    return True


def checkSign(dev_id, nonce, sign):
    appkey = settings.APPKEY_IOS
    
    if cache.get(sign) is None and sign == hashlib.md5(nonce + dev_id + appkey).hexdigest():
        cache.set(sign, True, 24 * 60 * 60)
        return True

    raise MyException(info='sign error') 

def isAppStoreChecking(version):
    if version == '1.1.1':
        return True
    return False      

def Init(request):
    ret = {}

    try:
        mac = request.POST.get('mac', '112233445566')
        dev_id = request.POST.get('dev_id')
        nonce = request.POST.get('nonce')
        token = request.POST.get('token')
        version = request.POST.get('version', '0.0.0')
        platform = request.POST.get('platform', 'ios')
        cs = request.POST.get('cs')

        checkParam(mac, dev_id, token)

        checkSign(dev_id, nonce, cs)

        users =  User.objects.filter(dev_id=dev_id)
        if len(users) > 0:
            user = users[0]
            if user.token != token:
                user.token=token
                user.save()
        else:
            user_id = generateUserId()
            user = User.objects.create(user_id=user_id, mac=mac, dev_id=dev_id, token=token, version=version, platform=platform)

        ret['user'] = user.toJSON()
        
        if isAppStoreChecking(version):
            ret['user']['checking'] = True
        else:
            ret['user']['checking'] = False  
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_PARAM)



def Update(request):
    ret = {}
    return SuccessResponse(ret)

def GetTopUser(request):
    ret = {}
    ret['users'] = []

    try:    
        num = int(request.REQUEST.get('number', 10))
        
        users = User.objects.all().order_by('-total_points')[:num]
        
        for u in users:
            ret['users'].append(u.toJSON())
        
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)


def RequireAuth(view):
    def new_view(request, *args, **kwargs):

        try:
            user_id = int(request.REQUEST.get('user_id'))
            #mac = request.REQUEST.get('mac')
            dev_id = request.REQUEST.get('dev_id')
            #token = request.REQUEST.get('token')
            nonce = request.REQUEST.get('nonce')
            cs = request.REQUEST.get('cs')

            user = User.objects.get(user_id=user_id, dev_id=dev_id)

            checkSign(dev_id, nonce, cs)
            
            request.META['USER'] = user
            return view(request, *args, **kwargs)

        except:
            return ErrorResponse(E_AUTH)

    return new_view   


def RequireSign(view):
    def new_view(request, *args, **kwargs):

        try:
            dev_id = request.REQUEST.get('dev_id')
            nonce = request.REQUEST.get('nonce')
            cs = request.REQUEST.get('cs')

            checkSign(dev_id, nonce, cs)

            return view(request, *args, **kwargs)
        except:
            return ErrorResponse(E_AUTH)

    return new_view


def SetScore(request):
    ret = {}

    try:
        user = request.META['USER']
        score = int(request.POST.get('score'))
        user.total_points = score
        user.save()
        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)



def CreateTestUsers(request):
    ret = {}
    ret['users'] = []

    try:

        num = int(request.POST.get('num', 10))

        for i in range(num):
            user_id = generateUserId()
            mac = RandomStr(rlen=16)
            dev_id = RandomStr(rlen=32)
            token = RandomStr(rlen=32)
            user = User.objects.create(user_id=user_id, mac=mac, dev_id=dev_id, token=token, is_test=True)
            ret['users'].append(user.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

def DeleteTestUsers(request):
    ret = {}

    try:
        users = User.objects.filter(is_test=True)

        for user in users:
            user.delete()
    except:
        pass

    return SuccessResponse(ret)


def ShowAllUser(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['users'] = []
        for u in users:
            ret['users'].append(u.toJSON())
    except:
        pass

    return SuccessResponse(ret)


def EnableUser(request):
    ret = {}

    try:
        user_id = request.POST.get('user_id')
        user = User.objects.get(user_id=user_id)
        user.is_enable = enable
        user.save()

    except:
        return ErrorResponse(E_PARAM)

    return SuccessResponse(ret)

