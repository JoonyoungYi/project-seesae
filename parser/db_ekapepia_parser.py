# -*- coding:utf-8 -*-
from urllib import urlopen
from urllib import urlencode
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
from datetime import datetime
from locale import getpreferredencoding

class EkapepiaDataRetriever:
    def __init__(self, fromDate, productName =''):
        self.systemCodePage = getpreferredencoding()
        self.productName = self.toUtf(productName)
        self.fromDate = self.dateManipulator(fromDate)
        self.outputProductClass = []
        if productName != '':
            for i in [self.toUtf('한우'), self.toUtf('육우')]:
                for j in ['1++', '1+', '1', '2', '3']:
                    self.outputProductClass.append((productName+'('+i+')', j))
        else:
            for i in ['1+', '1', '2']:
                self.outputProductClass.append((self.toUtf('돈육'), i))
        self.outputProductData = []
        
    def dateManipulator(self, date):
        assert isinstance(date, str)
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    def soupCooker(self):
        assert isinstance(self.productName, str)
        assert isinstance(self.fromDate, date)
        dateString = ''.join(self.fromDate.isoformat().split('-'))
        if self.productName.strip() == '':
            url = 'http://www.ekapepia.com/user/priceStat/periodPigAuctionPrice.do'
            data = {'startDate' : self.fromDate.isoformat(),
                    'endDate' : self.fromDate.isoformat(),
                    'sableGubn' : '3',
                    'judgeSex' : '4',
                    'searchGradeGubn' : '1'}
        else:
            url = 'http://www.ekapepia.com/user/priceStat/periodBeefAuctionPrice.do'
            data = {'startDate' : self.fromDate.isoformat(),
                    'endDate' : self.fromDate.isoformat(),
                    'abattCode' : '0000'}
        dt = urlencode(data)
        dt = dt.encode('utf-8')
        html = urlopen(url, dt)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def produceOutput(self):
        if self.productName.strip() != '':
            while self.fromDate - timedelta(days=1) != date.today():
                if self.fromDate.weekday() < 6:
                    s = self.soupCooker()
                    tbody = s.tbody
                    tr_child = tbody.findAll(name='tr')
                    for child in tr_child:
                        try:
                            if self.productName == child.th.string.strip().encode('utf-8'):
                                temp = []
                                td_c = child.findAll(name='td')
                                for c in td_c:
                                    if len(c.contents) == 1:
                                        temp.append('')
                                    else:
                                        temp.append(c.contents[0].string.encode('utf-8'))
                                for i in xrange(5):
                                    try:
                                        self.outputProductData.append((i, self.fromDate.isoformat(), int(''.join(temp[i].split(',')))))
                                    except:
                                        self.outputProductData.append((i, self.fromDate.isoformat(), 0))
                                for i in xrange(5):
                                    try:
                                        self.outputProductData.append((i, self.fromDate.isoformat(), int(''.join(temp[7+i].split(',')))))
                                    except:
                                        self.outputProductData.append((i, self.fromDate.isoformat(), 0))
                        except:
                            continue
                self.fromDate = self.fromDate + timedelta(days = 1)
        else:
            while self.fromDate - timedelta(days=1) != date.today():
                print str(self.fromDate)
                if self.fromDate.weekday() < 6:
                    s = self.soupCooker()
                    tbody = s.tbody
                    counter = 0
                    tr_child = tbody.findAll(name='tr')
                    for child in tr_child:
                        try:
                            if child.th.contents[0].strip().encode('utf-8').isdigit():
                                temp = []
                                td_c = child.findAll(name='td')
                                for c in td_c:
                                    if len(c.contents) != 2:
                                        temp.append('')
                                    else:
                                        temp.append(c.contents[0].string.encode('utf-8'))
                                try:
                                    self.outputProductData.append((counter, self.fromDate.isoformat(), int(''.join(temp[0].split(',')))))
                                except:
                                    self.outputProductData.append((counter, self.fromDate.isoformat(), 0))
                            counter += 1
                        except:
                            print 'ERROR!!'
                            continue
                self.fromDate = self.fromDate + timedelta(days = 1)
                
    def toUtf(self, input, defaultEncoding = 'cp949'):
        try:
            return input.decode(defaultEncoding).encode('utf-8')
        except:
            return input.decode(self.systemCodePage).encode('utf-8')