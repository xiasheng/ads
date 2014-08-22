

# -*- coding: utf-8 -*-  

from ads.views.common import *
from ads.models.models import QiuBai
from bs4 import BeautifulSoup
import re
import threading
import time
import requests

class SpiderThread(threading.Thread):
    def __init__(self, maxnum, maxpage):
        threading.Thread.__init__(self)
        self.maxnum = maxnum
        self.maxpage = maxpage
        
    def run(self):
        num = 0
        page = 1
        while num < self.maxnum and page <= self.maxpage:
        
          r = requests.get('http://www.qiushibaike.com/8hr/page/' + str(page))
          bs = BeautifulSoup(r.content)
          allqs = bs.find_all(id=re.compile('qiushi_tag_'))
        
          for qs in allqs:
              try:
                  id = qs.get('id').lstrip('qiushi_tag_')
                  content = qs.find('div', {'class' : 'content'} ).text.strip()
                  image = qs.find('div', {'class' : 'thumb'} )
                  if image:
                      image = image.find('img').get('src')
                  else:
                      image = ''      
        
                  if QiuBai.objects.filter(qid=id).count() > 0:
                      continue
                  else:
                      QiuBai.objects.create(qid=id, content=content, image=image)    
                      num += 1
              
              except :
                  pass
                  
          page += 1
          time.sleep(3)        
        

def Spider(request):
    ret = {}

    maxnum = int( request.GET.get('num', 100) )
    maxpage = int( request.GET.get('page', 100) )

    SpiderThread(maxnum, maxpage).start()
    
    return SuccessResponse(ret)
    
    
    
def QiuShi(request):
    ret = {}
    ret['records'] = []

    maxnum = int( request.GET.get('maxnum', 10) )
    maxid = int( request.GET.get('maxid', 99999999) )
    
    try:
        records = QiuBai.objects.filter(pk__lt=maxid).order_by('-id')[:maxnum]

        for r in records:
            ret['records'].append(r.toJSON())

        return SuccessResponse(ret)
    except:
        return ErrorResponse(E_SYSTEM)

