

from django.db import models
import time

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    dev_id = models.CharField(max_length=128)
    mac = models.CharField(max_length=32)
    token = models.CharField(max_length=128)
    total_points = models.IntegerField(default=0)
    password = models.CharField(max_length=128, null=True)
    nickname = models.CharField(max_length=64, default='')
    type = models.CharField(max_length=32, null=True)
    is_test = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True)
    time_created = models.IntegerField(default=int(time.time()))
    
    def toJSON(self):
        r = {}
        r['id'] = str(self.user_id)
        r['mac'] = self.mac
        r['openudid'] = self.dev_id
        r['token'] = self.token
        r['nickName'] = self.nickname
        r['totalPoints'] = self.total_points
        return r

    
class PointRecord(models.Model):
    user = models.ForeignKey('User')
    type = models.CharField(max_length=32, default='+')
    channel = models.CharField(max_length=64, default='')
    task = models.CharField(max_length=256, default='')
    point = models.IntegerField(default=0)
    status = models.CharField(max_length=32, default='')
    time_created = models.IntegerField(default=int(time.time()))    
    
    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['channel'] = self.channel
        r['task'] = self.task
        r['increase'] = self.point
        r['status'] = self.status
        r['createtime'] = self.time_created
        return r
        
            
class ExchangeRecord(models.Model):
    user = models.ForeignKey('User')
    type = models.CharField(max_length=32)
    account = models.CharField(max_length=128, null=True)
    cost = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    status = models.CharField(max_length=32)
    xid = models.CharField(max_length=64, null=True)
    time_created = models.IntegerField(default=int(time.time()))
    time_processed = models.IntegerField(default=int(time.time()))
    
    def toJSON(self):
        r = {}
        r['type'] = str(self.type)
        r['cost'] = self.cost
        r['amount'] = self.amount
        r['status'] = self.status
        r['createTime'] = self.time_created
        r['processingTime'] = self.time_processed
        return r
            
class Channel(models.Model):
    code = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=1024, null=True)
    name = models.CharField(max_length=64, null=True)
    image = models.CharField(max_length=128, null=True)
    order = models.IntegerField(default=0)    
        
    def toJSON(self):
        r = {}
        r['code'] = str(self.code)
        r['description'] = self.description
        r['name'] = self.name
        r['image'] = self.image
        r['order'] = self.order
        return r

class Adwo(models.Model):
    appid = models.CharField(max_length=128, null=True)
    adname = models.CharField(max_length=128, null=True)
    adid = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    idfa = models.CharField(max_length=128, null=True)
    androidid = models.CharField(max_length=128, null=True)
    imei = models.CharField(max_length=128, null=True)
    point = models.IntegerField(default=0)
    ts = models.IntegerField(default=0)
    
    def toJSON(self):
        r = {}
        r['appid'] = self.appid
        r['adname'] = self.adname
        r['adid'] = self.adid
        r['device'] = self.device
        r['idfa'] = self.idfa
        r['androidid'] = self.androidid
        r['imei'] = self.imei
        r['point'] = self.point
        r['ts'] = self.ts
        return r 

class Youmi(models.Model):
    type = models.CharField(max_length=32, null=True)
    order = models.CharField(max_length=128, null=True)
    app = models.CharField(max_length=128, null=True)
    ad = models.CharField(max_length=128, null=True)
    adid = models.CharField(max_length=128, null=True)
    user = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    chn = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    point = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    #time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['order'] = self.order
        r['app'] = self.app
        r['ad'] = self.ad
        r['adid'] = self.adid
        r['user'] = self.user
        r['device'] = self.device
        r['chn'] = self.chn
        r['price'] = str(self.price)
        r['point'] = self.point
        r['time'] = self.time
        return r  

class Miidi(models.Model):
    id = models.CharField(max_length=128, null=True)
    trand_no = models.CharField(max_length=128, null=True)
    cash = models.IntegerField(default=0)
    imei = models.CharField(max_length=128, null=True)
    bundleId = models.CharField(max_length=128, null=True)
    param0 = models.CharField(max_length=128, null=True)
    appName = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['id'] = self.id
        r['trand_no'] = self.trand_no
        r['cash'] = self.cash
        r['imei'] = self.imei
        r['bundleId'] = self.bundleId
        r['param0'] = self.param0
        r['appName'] = self.appName
        r['time_created'] = self.time_created
        return r 

