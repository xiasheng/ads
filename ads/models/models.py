
# -*- coding: utf-8 -*-  

from django.db import models
import time


def Now():
    return int(time.time())

class User(models.Model):
    user_id = models.IntegerField(primary_key=True, verbose_name = u'用户ID')
    dev_id = models.CharField(max_length=128, verbose_name = u'设备ID')
    mac = models.CharField(max_length=128)
    token = models.CharField(max_length=128)
    total_points = models.IntegerField(default=0, verbose_name = u'总积分')
    password = models.CharField(max_length=128, null=True)
    nickname = models.CharField(max_length=64, default='')
    version = models.CharField(max_length=32, default='0.0.0')
    status = models.CharField(max_length=32, default='ok')
    platform = models.CharField(max_length=32, default='ios')
    is_test = models.BooleanField(default=False)
    is_enable = models.BooleanField(default=True, verbose_name = u'账号状态')
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['user_id'] = str(self.user_id)
        r['mac'] = self.mac
        r['dev_id'] = self.dev_id
        r['token'] = self.token
        r['nickName'] = self.nickname
        r['platform'] = self.platform
        r['version'] = self.version
        r['status'] = self.status
        r['totalPoints'] = self.total_points
        return r

    def __unicode__(self):
        return str(self.user_id)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'
        #app_label = u'用户管理'
        #db_table = 'models_user'

class PointRecord(models.Model):
    user = models.ForeignKey('User', verbose_name = u'用户ID')
    type = models.CharField(max_length=32, default='+', verbose_name = u'类型')
    channel = models.CharField(max_length=64, default='', verbose_name = u'广告平台')
    task = models.CharField(max_length=256, default='', verbose_name = u'任务名称')
    point = models.IntegerField(default=0, verbose_name = u'积分')
    status = models.CharField(max_length=32, default='', verbose_name = u'状态')
    time_created = models.IntegerField(default=Now)    
    
    def toJSON(self):
        r = {}
        r['type'] = self.type
        r['channel'] = self.channel
        r['task'] = self.task
        r['increase'] = self.point
        r['status'] = self.status
        r['createtime'] = self.time_created
        return r

    class Meta:
        verbose_name = u'积分记录'
        verbose_name_plural = u'积分记录'
        #app_label = u'数据统计'
        #db_table = 'models_pointrecord' 

class ExchangeRecord(models.Model):
    user = models.ForeignKey('User', verbose_name = u'用户ID')
    type = models.CharField(max_length=32, verbose_name = u'兑换类型')
    account = models.CharField(max_length=128, null=True, verbose_name = u'账号')
    cost = models.IntegerField(default=0, verbose_name = u'消费积分')
    amount = models.IntegerField(default=0, verbose_name = u'兑换金额')
    status = models.CharField(max_length=32, verbose_name = u'状态')
    description = models.CharField(max_length=256, null=True)
    xid = models.CharField(max_length=64, null=True)
    time_created = models.IntegerField(default=Now)
    time_processed = models.IntegerField(default=Now)
    
    def toJSON(self):
        r = {}
        r['type'] = str(self.type)
        r['cost'] = self.cost
        r['amount'] = self.amount
        r['status'] = self.status
        r['description'] = self.description
        r['createTime'] = self.time_created
        r['processingTime'] = self.time_processed
        return r

    class Meta:
        verbose_name = u'兑换记录'
        verbose_name_plural = u'兑换记录'
        #app_label = u'数据统计' 
        #db_table = 'models_exchangerecord'

class ExchangeProduct(models.Model):
    code = models.CharField(max_length=64, verbose_name = u'产品代号')
    name = models.CharField(max_length=64, null=True, verbose_name=u'类型')
    price = models.IntegerField(default=0, verbose_name = u'价格')
    score = models.IntegerField(default=0, verbose_name = u'积分')
    info = models.CharField(max_length=64, verbose_name = u'描述')
    typeName = models.CharField(max_length=64, null=True)
    typeCode = models.CharField(max_length=64, null=True)
    typeLabel = models.CharField(max_length=64, null=True)

    def toJSON(self):
        r = {}
        r['code'] = str(self.code)
        r['name'] = self.name
        r['price'] = self.price
        r['score'] = self.score
        r['info'] = self.info
        r['typeName'] = self.typeName
        r['typeCode'] = self.typeCode
        r['typeLabel'] = self.typeLabel
        return r

    class Meta:
        verbose_name = u'兑换产品'
        verbose_name_plural = u'兑换产品'
            
class Channel(models.Model):
    code = models.CharField(max_length=64, null=True)
    description = models.CharField(max_length=1024, null=True, verbose_name = u'描述')
    name = models.CharField(max_length=64, null=True, verbose_name = u'名称')
    image = models.CharField(max_length=128, null=True)
    order = models.IntegerField(default=0, verbose_name = u'优先级')
    tasknum = models.IntegerField(default=10)
    is_enable = models.BooleanField(default=True, verbose_name = u'激活状态')

    def toJSON(self):
        r = {}
        r['id'] = self.id
        r['order'] = self.order
        r['code'] = str(self.code)
        r['description'] = self.description
        r['name'] = self.name
        r['image'] = self.image 
        return r

    class Meta:
        verbose_name = u'广告平台'
        verbose_name_plural = u'广告平台'
        ordering=['order']

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
    time_created = models.IntegerField(default=Now)
    
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
    time_created = models.IntegerField(default=Now)

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
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['id'] = self.adid
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
    time_created = models.IntegerField(default=Now)

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
    time_created = models.IntegerField(default=Now)

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
    time_created = models.IntegerField(default=Now)

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
    time_created = models.IntegerField(default=Now)

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
    time_created = models.IntegerField(default=Now)

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

class Yijifen(models.Model):
    type = models.CharField(max_length=32, null=True)
    uuid  = models.CharField(max_length=128, null=True)
    userId = models.CharField(max_length=128, null=True)
    score = models.IntegerField(default=0)
    exchangetime = models.CharField(max_length=128, null=True)
    plat = models.CharField(max_length=128, null=True)
    idfa = models.CharField(max_length=128, null=True)
    appName = models.CharField(max_length=128, null=True)
    adId = models.CharField(max_length=128, null=True)
    adName = models.CharField(max_length=256, null=True)
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['uuid'] = self.uuid
        r['userId'] = self.userId
        r['score'] = self.score
        r['exchangetime'] = self.exchangetime
        r['plat'] = self.plat
        r['idfa'] = self.idfa
        r['appName'] = self.appName
        r['adId'] = self.adId
        r['adName'] = self.adName
        return r

class Dianjoy(models.Model):
    type = models.CharField(max_length=32, null=True)
    snuid  = models.CharField(max_length=128, null=True)
    device_id = models.CharField(max_length=128, null=True)
    app_id = models.CharField(max_length=128, null=True)
    currency = models.IntegerField(default=0)
    app_ratio = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    time_stamp = models.CharField(max_length=128, null=True)
    ad_name = models.CharField(max_length=256, null=True)
    pack_name = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['snuid'] = self.snuid
        r['device_id'] = self.device_id
        r['app_id'] = self.app_id
        r['currency'] = self.currency
        r['app_ratio'] = str( self.app_ratio )
        r['time_stamp'] = self.time_stamp
        r['ad_name'] = self.ad_name
        r['pack_name'] = self.pack_name
        return r

class Chukong(models.Model):
    type = models.CharField(max_length=32, null=True)
    os  = models.CharField(max_length=32, null=True)
    os_version = models.CharField(max_length=32, null=True)
    idfa = models.CharField(max_length=128, null=True)
    mac = models.CharField(max_length=32, null=True)
    imei = models.CharField(max_length=128, null=True)
    ip = models.CharField(max_length=32, null=True)
    transactionid = models.CharField(max_length=128, null=True)
    coins = models.IntegerField(default=0)
    adid = models.CharField(max_length=128, null=True)
    adtitle = models.CharField(max_length=256, null=True)
    taskname = models.CharField(max_length=256, null=True)
    taskcontent = models.CharField(max_length=256, null=True)
    token = models.CharField(max_length=128, null=True)
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['os'] = self.os
        r['os_version'] = self.os_version
        r['idfa'] = self.idfa
        r['mac'] = self.mac
        r['imei'] = str( self.imei )
        r['ip'] = self.ip
        r['transactionid'] = self.transactionid
        r['coins'] = self.coins
        r['adid'] = self.adid
        r['adtitle'] = self.adtitle
        r['taskname'] = self.taskname
        r['taskcontent'] = self.taskcontent
        r['token'] = self.token
        return r

class Mopan(models.Model):
    type = models.CharField(max_length=32, null=True)
    imei  = models.CharField(max_length=128, null=True)
    param0 = models.CharField(max_length=128, null=True)
    cash = models.IntegerField(default=0)
    trand_no = models.CharField(max_length=128, null=True)
    adid = models.CharField(max_length=128, null=True)
    appShowName = models.CharField(max_length=256, null=True)
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['imei'] = self.imei
        r['param0'] = self.param0
        r['cash'] = self.cash
        r['trand_no'] = self.trand_no
        r['adid'] = self.adid
        r['appShowName'] = self.appShowName
        return r

class ZhuanPanRecord(models.Model):
    user = models.ForeignKey('User')
    point = models.IntegerField(default=0)
    angle = models.IntegerField(default=0)
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['point'] = self.point
        r['angle'] = self.angle
        r['createtime'] = self.time_created
        return r


class QiuBai(models.Model):
    qid = models.CharField(max_length=32, default='')
    content = models.CharField(max_length=1024, default='')
    image = models.CharField(max_length=256, default='')
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['id'] = self.id
        r['content'] = self.content
        r['image'] = self.image
        #r['createtime'] = self.time_created
        return r

class Duiba(models.Model):
    appKey = models.CharField(max_length=64, null=True)
    timestamp  = models.CharField(max_length=64, null=True)
    uid = models.CharField(max_length=64, null=True)
    credits = models.IntegerField(default=0)
    description = models.CharField(max_length=128, null=True, default='')
    orderNum = models.CharField(max_length=128, null=True)
    dtype = models.CharField(max_length=64, null=True)
    facePrice = models.IntegerField(default=0)
    actualPrice = models.IntegerField(default=0)
    alipay = models.CharField(max_length=128, null=True, default='')
    phone = models.CharField(max_length=128, null=True, default='')
    qq = models.CharField(max_length=128, null=True, default='')
    waitAudit = models.BooleanField(default=False)
    status = models.CharField(max_length=128, null=True, default='')
    message = models.CharField(max_length=128, null=True, default='')
    time_created = models.IntegerField(default=Now)

    def toJSON(self):
        r = {}
        r['timestamp'] = self.timestamp
        r['uid'] = self.uid
        r['credits'] = self.credits
        r['description'] = self.description
        r['orderNum'] = self.orderNum
        r['type'] = self.dtype
        r['facePrice'] = self.facePrice
        r['actualPrice'] = self.actualPrice
        r['alipay'] = self.alipay
        r['phone'] = self.phone
        r['qq'] = self.qq
        r['waitAudit'] = self.waitAudit
        r['status'] = self.status
        r['message'] = self.message

        return r
