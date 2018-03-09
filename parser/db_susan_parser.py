# -*- coding:utf-8 -*-
from urllib import urlopen
from urllib import urlencode
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
from datetime import datetime
from locale import getpreferredencoding

class SusanDataRetriever:
    def __init__(self, keyName, eKeyName, productName, fromDate):
        self.systemCodePage = getpreferredencoding()
        self.keyName = self.toUtf(keyName)
        self.eKeyName = self.toUtf(eKeyName)
        self.productName = self.toUtf(productName)
        self.fromDate = self.dateManipulator(fromDate)
        self.outputProductData = []
        self.outputProductClass = []
        
    def dateManipulator(self, date):
        assert isinstance(date, str)
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    def soupCooker(self):
        assert isinstance(self.keyName, str)
        assert isinstance(self.eKeyName, str)
        assert isinstance(self.productName, str)
        assert isinstance(self.fromDate, date)
        dateString = ''.join(self.fromDate.isoformat().split('-'))
        url = 'http://www.susansijang.co.kr/cost/todayCost.do'
        data = {'auctdt' : dateString,
                'keyname' : self.keyName,
                'ekeyname' : self.eKeyName,
                'pageno' : '0',
                'pagesize' : '200'}
        dt = urlencode(data)
        dt = dt.encode('utf-8')
        html = urlopen(url, dt)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def produceOutput(self):
        while self.fromDate - timedelta(days=1) != date.today():
            print str(self.fromDate)
            if self.fromDate.weekday() < 6:
                s = self.soupCooker()
                tbody = s.tbody
                tr_child = tbody.findAll(name='tr')
                for child in tr_child:
                    try:
                        if self.productName == child.td.string.split(')')[1].strip().encode('utf-8'):
                            temp = []
                            td_child = child.findAll(name='td')
                            for c in td_child:
                                temp.append(c.string)
                            classTup = (temp[0].encode('utf-8'), (temp[1]+'('+temp[2]+')').encode('utf-8'))
                            if classTup in self.outputProductClass:
                                i = self.outputProductClass.index(classTup)
                                dataTup = (i, self.fromDate.isoformat(), int(''.join(temp[7].split(','))))
                                self.outputProductData.append(dataTup)
                            else:
                                i = len(self.outputProductClass)
                                self.outputProductClass.append(classTup)
                                dataTup = (i, self.fromDate.isoformat(), int(''.join(temp[7].split(','))))
                                self.outputProductData.append(dataTup)
                    except: 
                        print 'ERROR!!'
                        continue
            self.fromDate = self.fromDate + timedelta(days = 1)
            
    def toUtf(self, input, defaultEncoding = 'cp949'):
        try:
            return input.decode(defaultEncoding).encode('utf-8')
        except:
            return input.decode(self.systemCodePage).encode('utf-8')
