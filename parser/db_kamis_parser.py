# -*- coding:utf-8 -*-
from urllib import urlopen
from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
from datetime import datetime

class KamisDataRetriever:
    def __init__(self, retrieveCategory, retrieveItem, fromDate, kindCode = ''):
        self.retrieveCategory = retrieveCategory
        self.retrieveItem = retrieveItem
        self.kindCode = kindCode
        self.fromDate = self.dateManipulator(fromDate)
        
    def dateManipulator(self, date):
        assert isinstance(date, str)
        return datetime.strptime(date, '%Y-%m-%d').date()
    
    def soupCooker(self):
        assert isinstance(self.retrieveCategory, str)
        assert isinstance(self.retrieveItem, str)
        assert isinstance(self.kindCode, str)
        assert isinstance(self.fromDate, date)
        url = 'https://www.kamis.co.kr/customer/price/retail/item.do?regday='+self.fromDate.isoformat()+'&itemcategorycode='+self.retrieveCategory + '&itemcode='+self.retrieveItem+'&kindcode='+self.kindCode
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def produceOutput(self):
        l = []
        while self.fromDate - timedelta(days=1) != date.today():
            print self.fromDate
            cat = 0
            if self.fromDate.weekday() < 5:
                s = self.soupCooker()
                div = s.table.parent
                table_child = div.findAll(name='table')
                for child in table_child:
                    try:
                        temp = []
                        td_c = child.tbody.tr.findAll(name='td')
                        for c in td_c:
                            temp.append(c.string)
                        if len(temp) >2:
                            tup = (cat, self.fromDate.isoformat(), int(''.join(temp[1].split(','))))
                            l.append(tup)
                        else:
                            tup = (cat, self.fromDate.isoformat(), 0)
                            l.append(tup)
                        cat += 1
                    except:
                        print 'ERROR!!'
                        continue
            self.fromDate = self.fromDate + timedelta(days = 1)
        return l
    
    def productClassList(self):
        l = []
        s = self.soupCooker()
        div = s.table.parent
        table_child = div.findAll(name='table') 
        for child in table_child:
            caption = child.caption.span.string.split('>')
            tup = (caption[4].strip().encode('utf-8'), caption[5].strip().encode('utf-8'))
            l.append(tup)
        return l
