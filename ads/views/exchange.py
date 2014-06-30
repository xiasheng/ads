
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import ExchangeRecord, User
from django.conf import settings
import re, threading, hashlib, time
from django.http import HttpResponse
from urllib import urlencode


def checkTelPhone(tel):
    p = re.compile(r'((^13[0-9]|15[0|3|6|7|8|9]|18[8|9])\d{8}$)')
    if tel and p.match(tel):
        return True
    raise MyException(info='illegal telphone')

def checkQQ(qq):
    if qq and int(qq) >=1000 and int(qq) <= 999999999999:
        return True

    raise MyException(info='illegal qqNumber')

def checkAliNo(aliNo):
    if aliNo and len(aliNo) > 6 and len(aliNo) < 64:
        return True

    raise MyException(info='illegal aliNo')

def checkCost(cost, amount):
    if cost > 0 and amount > 0 and cost >= amount:
        return True
    raise MyException(info='illegal cost and amount')

class notifythread(threading.Thread):
    def __init__(self, title, content):
        threading.Thread.__init__(self)
        self.title = title
        self.content = content
    def run(self):
        notifyEmail(self.title, self.content)

def notifyEmail(title, content):
    from django.core.mail import send_mail, EmailMessage
    #send_mail(title, content, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENTS, fail_silently=False)
    msg = EmailMessage(title, content, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENTS)
    msg.content_subtype = 'html'
    msg.send()

def getXid():
  return RandomStr(rlen=32)

def ExTelPhone(request):
    ret = {}

    try:
        user = request.META['USER']
        telphone = request.POST.get('telphone')
        amount = int(request.POST.get('amount'))
        cost = int(request.POST.get('cost'))

        checkTelPhone(telphone)
        checkCost(cost, amount)

        if cost > user.total_points:
            return ErrorResponse(E_SYSTEM, info='亲，您的积分不够用了，要再努力点哦')

        user.total_points -= cost
        user.save()

        r = ExchangeRecord.objects.create(user=user, type='telphone', account=telphone,
        cost=cost, amount=amount, status='pending', xid=getXid())
        
        sendNotifyEmail('telphone', telphone, cost, amount, request.get_host(), user.user_id, r.xid, r.time_created)

        return SuccessResponse(ret)
    except MyException, e:
        return ErrorResponse(E_SYSTEM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)

def ExQb(request):
    ret = {}

    try:
        user = request.META['USER']
        qq = request.POST.get('qqNumber')
        amount = int(request.POST.get('amount'))
        cost = int(request.POST.get('cost'))

        checkQQ(qq)
        checkCost(cost, amount)

        if cost > user.total_points:
            return ErrorResponse(E_SYSTEM, info='亲，您的积分不够用了，要再努力点哦')

        user.total_points -= cost
        user.save()

        r = ExchangeRecord.objects.create(user=user, type='qb', account=qq,
        cost=cost, amount=amount, status='pending', xid=getXid())

        sendNotifyEmail('qb', qq, cost, amount, request.get_host(), user.user_id, r.xid, r.time_created)

        return SuccessResponse(ret)
    except MyException, e:
        return ErrorResponse(E_SYSTEM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)


def ExAlipay(request):
    ret = {}

    try:
        user = request.META['USER']
        aliNo = request.POST.get('alipayNo')
        amount = int(request.POST.get('amount'))
        cost = int(request.POST.get('cost'))

        checkAliNo(aliNo)
        checkCost(cost, amount)

        if cost > user.total_points:
            return ErrorResponse(E_SYSTEM, info='亲，您的积分不够用了，要再努力点哦')

        user.total_points -= cost
        user.save()

        r = ExchangeRecord.objects.create(user=user, type='alipay', account=aliNo,
        cost=cost, amount=amount, status='pending', xid=getXid())

        sendNotifyEmail('alipay', aliNo, cost, amount, request.get_host(), user.user_id, r.xid, r.time_created)

        return SuccessResponse(ret)
    except MyException, e:
        return ErrorResponse(E_SYSTEM, e.info)
    except:
        return ErrorResponse(E_SYSTEM)

def ExRecord(request):
    ret = {}
    ret['records'] = []

    try:
        user = request.META['USER']
        records = ExchangeRecord.objects.filter(user=user)

        for r in records:
            ret['records'].append(r.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)


def getConfirmUrl(host, uid, xid, t):
    uid = str(uid)
    xid = str(xid)
    t = str(t)
    cs = hashlib.md5('ex_confirm'+uid+xid+t).hexdigest()
    url = 'http://%s/exconfirm/?uid=%s&xid=%s&t=%s&cs=%s' %(host, uid, xid, t, cs)
    return url
    
def getProblemUrl(host, uid, xid, t):
    uid = str(uid)
    xid = str(xid)
    t = str(t)
    cs = hashlib.md5('ex_problem'+uid+xid+t).hexdigest()
    url = 'http://%s/exproblem/?uid=%s&xid=%s&t=%s&cs=%s' %(host, uid, xid, t, cs)
    return url    


def sendNotifyEmail(type, account, cost, amount, host, uid, xid, t):
    if type == 'telphone':
        title = u'【兑换话费】 用户ID:' + str(uid) + u'  手机号:' + account + u'  使用积分:' + str(cost) + u'  兑换金额:' + str(amount)
    elif type == 'qb':
        title = u'【兑换Q币】 用户ID:' + str(uid) + u'  QQ号:' + account + u'  使用积分:' + str(cost) + u'  兑换金额:' + str(amount)        
    elif type == 'alipay':
        title = u'【兑换支付宝】 用户ID:' + str(uid) + u'  支付宝号:' + account + u'  使用积分:' + str(cost) + u'  兑换金额:' + str(amount)        
    else:
        return
                    
    url1 = getConfirmUrl(host, uid, xid, t)
    url2 = getProblemUrl(host, uid, xid, t)
    content =  '<p>' +  u'成功支付请点击该链接确认: ' + '<a href=' + url1 + '> <b>' + u'成功支付' + '</b> </a>' + '</p>'
    content += '<p>' +  u'遇到问题请点击该链接反馈: ' + '<a href=' + url2 + '> <b>' + u'遇到问题' + '</b> </a>' + '</p>'
    notifythread(title, content).start()


def ExConfirm(request):
    ret = {}
    ret['records'] = []

    try:
        uid = request.GET.get('uid')
        xid = request.GET.get('xid')
        t = request.GET.get('t')
        cs = request.GET.get('cs')

        if cs != hashlib.md5('ex_confirm'+uid+xid+t).hexdigest():
            return HttpResponse(u'无效链接')

        user = User.objects.get(user_id=uid)
        record = ExchangeRecord.objects.get(user=user, xid=xid, time_created=t)
        if record.status == 'pending':
            record.status = 'closed'
            record.time_processed  = int(time.time())
            record.save()
            return HttpResponse(u'确认支付成功')
        elif record.status == 'closed':
            return HttpResponse(u'该交易已经结束了哦')
        else:
            return HttpResponse(u'系统错误')

    except:
        return HttpResponse(u'无效链接')
        

def ExProblem(request):
    ret = {}
    ret['records'] = []

    try:
        uid = request.GET.get('uid')
        xid = request.GET.get('xid')
        t = request.GET.get('t')
        cs = request.GET.get('cs')
        flag = request.GET.get('flag', '0')
        problem = request.POST.get('problem', '')
        
        if cs != hashlib.md5('ex_problem'+uid+xid+t).hexdigest():
            return HttpResponse(u'无效链接')
            
        if flag == '0':
            action = '/exproblem/?flag=1&' + urlencode(request.GET)
            html = '<form action=%s method="post">  <p>Write your problem here:</p><textarea rows="5" cols="80" name="problem"> </textarea>  <p><input type="submit" value="Submit" /></p> </form>' %(action)
            return HttpResponse(html)    

        user = User.objects.get(user_id=uid)
        record = ExchangeRecord.objects.get(user=user, xid=xid, time_created=t)
        if record.status == 'pending':
            record.status = 'failed'
            record.description = problem
            record.time_processed  = int(time.time())
            record.save()
            return HttpResponse(u'提交问题反馈成功')
        elif record.status == 'closed':
            return HttpResponse(u'该交易已经结束了哦')
        else:
            return HttpResponse(u'系统错误')

    except:
        return HttpResponse(u'无效链接')    

