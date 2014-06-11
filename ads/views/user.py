

from ads.views.common import *
from ads.models.models import User
import random

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

def Init(request):
    ret = {}

    try:
        mac = request.POST.get('mac')
        dev_id = request.POST.get('openUdid')
        token = request.POST.get('token')
        
        checkParam(mac, dev_id, token)
        
        users =  User.objects.filter(mac=mac, dev_id=dev_id)
        if len(users) > 0:
            user = users[0]
        else:
            user_id = generateUserId()
            user = User.objects.create(user_id=user_id, mac=mac, dev_id=dev_id, token=token)
        
        ret['user'] = user.toJSON()
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
            user_id = request.REQUEST.get('userId')
            mac = request.REQUEST.get('mac')
            dev_id = request.REQUEST.get('openUdid')
            token = request.REQUEST.get('token')

            user = User.objects.get(user_id=user_id, mac=mac, dev_id=dev_id, token=token)
            request.META['USER'] = user
            return view(request, *args, **kwargs)
           
        except IOError:
            return ErrorResponse(E_AUTH)

    return new_view   

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


def ShowAllAccounts(request):
    ret = {}
    try:
        count = User.objects.all().count()
        users = User.objects.all()
        ret['count'] = count
        ret['ids'] = []
        for u in users:
            ret['users'].append(u.user_id)
    except:
        pass

    return SuccessResponse(ret)


def EnableAccount(request):
    ret = {}

    try:
        user_id = request.POST.get('user_id')
        user = User.objects.get(user_id=user_id)
        user.is_enable = enable
        user.save()

    except:
        return ErrorResponse(E_PARAM)

    return SuccessResponse(ret)
