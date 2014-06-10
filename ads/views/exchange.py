
# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import ExchangeRecord
import re

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
        
        ExchangeRecord.objects.create(user=user, type='telphone', account=telphone,
        cost=cost, amount=amount, status='pending')
                
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
        
        ExchangeRecord.objects.create(user=user, type='qb', account=qq,
        cost=cost, amount=amount, status='pending')
                
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
        
        ExchangeRecord.objects.create(user=user, type='alipay', account=aliNo,
        cost=cost, amount=amount, status='pending')
                
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


