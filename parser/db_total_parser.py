# -*- coding:utf-8 -*-
from db_kamis_parser import KamisDataRetriever
from db_susan_parser import SusanDataRetriever
from db_ekapepia_parser import EkapepiaDataRetriever

class SampleRetriever:
    
    def __init__(self, fromDate):
        self.fromDate = fromDate
        self.susanCategory = []
        self.susanData = []
        self.kamisCategory = []
        self.kamisData = []
        self.ekapepiaCategory = []
        self.ekapepiaData = []
        
    def sampleSusan(self):
        sampleList = [('가','낗','깐굴'), ('바','삫','바위굴'), ('다','띻','돌꼬막'), ('사','앃','새꼬막'), ('차','칳','참꼬막'), ('파','핗','피꼬막'), ('가','낗','꽁치'), ('아','잏','암꽃개'),
                      ('사','앃','수꽃개'), ('나','닣','넙치'), ('나','닣','낙지'), ('가','낗','겉바지락'), ('가','낗','깐바지락'), ('마','밓','물바지락'), ('바','삫','봉바지락'), ('카','킿','칼바지락'),
                      ('타','팋','토바지락'), ('아','잏','오징어'), ('바','삫','백조기'), ('바','삫','부세'), ('사','앃','수조기'), ('자','찧','조기'), ('차','칳','참조기'), ('하','힣','황석어'),]
        for keyName, eKeyName, productName in sampleList:
            a = SusanDataRetriever(keyName, eKeyName, productName, self.fromDate)
            a.produceOutput()
            l = len(self.susanCategory)
            for cat, dat, pri in a.outputProductData:
                self.susanData.append((cat + l, dat, pri))
            self.susanCategory += a.outputProductClass

    def sampleKamis(self):
        sampleList = [(200, 211, ''), (300, 315, '00'), (400, 411, '05'), (400, 412, '01'), (400, 415, '00'), (400, 418, '02'), (400, 421, '04'), (200, 226, '00'), (200, 221, '00')]
        for catCode, itemCode, kindCode in sampleList:
            a = KamisDataRetriever(str(catCode), str(itemCode), self.fromDate, kindCode)
            b = a.produceOutput()
            l = len(self.kamisCategory)
            for cat, dat, pri in b:
                self.kamisData.append((cat + l, dat, pri))
            self.kamisCategory += a.productClassList()

    def sampleEkapepia(self):
        sampleList = ['', '안심', '등심', '갈비', '사골', '꼬리', '양지', '사태']
        for productName in sampleList:
            a = EkapepiaDataRetriever(self.fromDate, productName)
            a.produceOutput()
            l = len(self.ekapepiaCategory)
            for cat, dat, pri in a.outputProductData:
                self.ekapepiaData.append((cat + l, dat, pri))
            self.ekapepiaCategory += a.outputProductClass
