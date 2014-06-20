

from django.db import models
import time

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    dev_id = models.CharField(max_length=128)
    mac = models.CharField(max_length=128)
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
        r['user_id'] = str(self.user_id)
        r['mac'] = self.mac
        r['dev_id'] = self.dev_id
        r['token'] = self.token
        r['nickName'] = self.nickname
        r['type'] = self.type
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
    tasknum = models.IntegerField(default=10)
        
    def toJSON(self):
        r = {}
        r['code'] = str(self.code)
        r['description'] = self.description
        r['name'] = self.name
        r['image'] = self.image
        r['order'] = self.order
        return r

class Adwo(models.Model):
    type = models.CharField(max_length=32, null=True)
    appid = models.CharField(max_length=128, null=True)
    adname = models.CharField(max_length=256, null=True)
    adid = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    idfa = models.CharField(max_length=128, null=True)
    androidid = models.CharField(max_length=128, null=True)
    imei = models.CharField(max_length=128, null=True)
    point = models.IntegerField(default=0)
    ts = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))
    
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
    ad = models.CharField(max_length=256, null=True)
    adid = models.CharField(max_length=128, null=True)
    user = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    chn = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    point = models.IntegerField(default=0)
    ts = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

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
        r['ts'] = self.ts
        return r  

class Miidi(models.Model):
    type = models.CharField(max_length=32, null=True)
    adid = models.CharField(max_length=128, null=True)
    trand_no = models.CharField(max_length=128, null=True)
    cash = models.IntegerField(default=0)
    imei = models.CharField(max_length=128, null=True)
    bundleId = models.CharField(max_length=128, null=True)
    param0 = models.CharField(max_length=128, null=True)
    appName = models.CharField(max_length=256, null=True)
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

class Domob(models.Model):
    type = models.CharField(max_length=32, null=True)
    orderid = models.CharField(max_length=128, null=True)
    pubid = models.CharField(max_length=128, null=True)
    ad = models.CharField(max_length=256, null=True)
    adid = models.CharField(max_length=128, null=True)
    user = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    channel = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    point = models.IntegerField(default=0)
    ts = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['orderid'] = self.orderid
        r['pubid'] = self.pubid
        r['ad'] = self.ad
        r['adid'] = self.adid
        r['user'] = self.user
        r['device'] = self.device
        r['channel'] = self.channel
        r['price'] = str(self.price)
        r['point'] = self.point
        r['ts'] = self.ts
        return r

class Guomob(models.Model):
    type = models.CharField(max_length=32, null=True)
    order = models.CharField(max_length=128, null=True)
    app = models.CharField(max_length=128, null=True)
    ad = models.CharField(max_length=256, null=True)
    adsid = models.CharField(max_length=128, null=True)
    device = models.CharField(max_length=128, null=True)
    mac = models.CharField(max_length=128, null=True)
    idfa = models.CharField(max_length=128, null=True)
    openudid = models.CharField(max_length=128, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    points = models.IntegerField(default=0)
    ts = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['order'] = self.order
        r['app'] = self.app
        r['ad'] = self.ad
        r['adsid'] = self.adsid
        r['device'] = self.device
        r['mac'] = self.mac
        r['idfa'] = self.idfa
        r['openudid'] = self.openudid
        r['price'] = str(self.price)
        r['points'] = self.points
        r['ts'] = self.ts
        return r 

class Mobsmar(models.Model):
    type = models.CharField(max_length=32, null=True)
    appid = models.CharField(max_length=128, null=True)
    userid = models.CharField(max_length=128, null=True)
    jobid = models.CharField(max_length=128, null=True)
    tid = models.CharField(max_length=128, null=True)
    imei = models.CharField(max_length=128, null=True)
    mac = models.CharField(max_length=128, null=True)
    idfa = models.CharField(max_length=128, null=True)
    openudid = models.CharField(max_length=128, null=True)
    points = models.IntegerField(default=0)
    appname = models.CharField(max_length=256, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['appid'] = self.appid
        r['userid'] = self.userid
        r['jobid'] = self.jobid
        r['tid'] = self.tid
        r['imei'] = self.imei
        r['mac'] = self.mac
        r['idfa'] = self.idfa
        r['openudid'] = self.openudid
        r['points'] = self.points
        r['appname'] = self.appname
        return r


class Waps(models.Model):
    type = models.CharField(max_length=32, null=True)
    adv_id = models.CharField(max_length=128, null=True)
    app_id = models.CharField(max_length=128, null=True)
    key = models.CharField(max_length=128, null=True)
    udid = models.CharField(max_length=128, null=True)
    open_udid = models.CharField(max_length=128, null=True)
    bill = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    points = models.IntegerField(default=0)
    ad_name = models.CharField(max_length=256, null=True)
    status = models.CharField(max_length=128, null=True)
    activate_time = models.CharField(max_length=128, null=True)
    order_id = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['adv_id'] = self.adv_id
        r['app_id'] = self.app_id
        r['key'] = self.key
        r['udid'] = self.udid
        r['open_udid'] = self.open_udid
        r['bill'] = str(self.bill)
        r['points'] = self.points
        r['ad_name'] = self.ad_name
        r['status'] = self.status
        r['activate_time'] = self.activate_time
        r['order_id'] = self.order_id
        return r 

class Dianru(models.Model):
    type = models.CharField(max_length=32, null=True)
    hashid = models.CharField(max_length=128, null=True)
    appid = models.CharField(max_length=128, null=True)
    adid = models.CharField(max_length=128, null=True)
    adname = models.CharField(max_length=256, null=True)
    userid = models.CharField(max_length=128, null=True)
    deviceid = models.CharField(max_length=128, null=True)
    source = models.CharField(max_length=128, null=True)
    point = models.IntegerField(default=0)
    ts = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=int(time.time()))

    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['hashid'] = self.hashid
        r['appid'] = self.appid
        r['adid'] = self.adid
        r['adname'] = self.adname
        r['userid'] = self.userid
        r['deviceid'] = self.deviceid
        r['source'] = self.source
        r['point'] = self.point
        r['ts'] = self.ts
        return r

