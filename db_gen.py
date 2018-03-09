# -*- coding:utf-8 -*-
"""
This code is origined in http://zetcode.com/db/mysqlpython/
Modified By Joonyoung Yi.
"""
from db_utils import parsed2proper
from config import *
from db import *
import random, datetime, math, csv

# -----------------------------------------------------------------------------
# GLOBAL VARIABLES
# -----------------------------------------------------------------------------
product_classes = [ ]
products = [    ('배추', 1, 'qocn.jpg' ), \
                ('느타리버섯', 1, 'smxkflqjtjt.jpg' ), \
                ('사과', 1, 'tkrhk.jpg' ), \
                ('배', 1, 'qo.jpg' ), \
                ('감귤', 1, 'rkarbf.jpg' ), \
                ('바나나', 1, 'qksksk.jpg' ), \
                ('오렌지', 1, 'dhfpswl.jpg' ), \
                ('딸기', 1, 'Ekfrl.jpg' ), \
                ('수박', 1, 'tnqkr.jpg' ), \
                ('굴', 2, 'qkdnlrnf.jpg' ), \
                ('꼬막', 2, 'toRhakr.jpg' ), \
                ('넙치', 2, 'sjqcl.jpg' ), \
                ('낙지', 2, 'skrwl.jpg' ), \
                ('바지락', 2, 'qkwlfkr.jpg' ), \
                ('오징어', 2, 'dhwlddj.jpg' ), \
                ('조기', 2, 'whrl.jpg' ), \
                ('돼지고기', 3, 'ehowlrhrl.jpg' ), \
                ('안심(소고기)', 3, 'dkstla.jpg' ), \
                ('등심(소고기)', 3, 'emdtla.jpg' ), \
                ('갈비(소고기)', 3, 'rkfql.jpg' ), \
                ('사골(소고기)', 3, 'tkrhf.jpg' ), \
                ('꼬리(소고기)', 3, 'Rhfl.jpg' ), \
                ('양지(소고기)', 3, 'didwl.jpg' ), \
                ('사태(소고기)', 3, 'tkxo.jpg' ) ]
product_max = len(products)
user_max = 20
store_max = 30

# -----------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------
def get_product_id_by_name(name):
    for i, product in enumerate(products):
        if product[0] == name:
            return i + 1
    return None

def get_product_class_id_by_name(cur, product_id, name):
    if (product_id, name) in product_classes:
        return product_classes.index((product_id, name)) + 1
        
    db_insert_product_class(cur, name, 0, product_id)
    product_classes.append((product_id, name))
    return len(product_classes) 
    
# -----------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------
con = db_connect()
db_init(con)
with con:
    cur = con.cursor()

    """
    INSERT PRODUCT INFORMATION
    """
    for i in range(1, product_max + 1):
        
        #
        product = products[i-1]

        #
        product_type = product[1]
        
        season_start_month = random.randint(1, 12)
        season_start_day = random.randint(1, 28)
        season_end_month = (season_start_month + 3) % 12
        season_end_day = season_start_day

        db_insert_product(cur, product_type, product[0], \
                              '../static/'+ product[2], \
                              '1000-'+str(season_start_month)+'-'+str(season_start_day), \
                              '1000-'+str(season_end_month)+'-'+str(season_end_day))

    """
    INSERT USER INFO
    """
    for i in range(1, user_max + 1):
        db_insert_user(cur, 'EMAIL%d@kaist.ac.kr' % i, 'PASSWORD%d' % i)

    """
    INSERT COMMENT INFO
    """
    for i in range(1, product_max + 1) :
        for j in range(1, user_max + 1) :
            content = "COMMENT_EXAMPLE_%d " % random.randint(0, 1000)
            content_r = ''
            for r in range(1, random.randint(2, 10)):
                content_r += content
            db_insert_comment(cur, j, i, content_r)
            
            p = random.random()
            if   p < 0.3 :
                db_insert_hate(cur, j, i)
            elif p < 0.6 :
                db_insert_favorite(cur, j, i)

    """
    INSERT STORE INFO
    """
    for i in range(1, store_max + 1):
        db_insert_store(cur, "STORE_%d" % i, 36.361627 + random.gauss(0, 1), 127.378329 + random.gauss(0, 1))

    """
    MAKE RELATION BETWEEN STORE AND PRODUCT
    """
    for i in range(1, store_max + 1):
        for j in range(1, product_max + 1):
            if random.random() < 0.5 :
                db_insert_product_store_relation(cur, j, i)

    """
    MAKE SIMILAR PRODUCT RELATION
    """
    for i in range(0, product_max):
        for j in range(i+1, product_max):
            if i != j and products[i][1] == products[j][1] :
                if random.random() < 0.3 :
                    db_insert_similar_product_relation(cur, i+1, j+1)
                    db_insert_similar_product_relation(cur, j+1, i+1)

    """

    """
    f_data = open('parser/data.csv', "rb")
    r_data = csv.reader(f_data, delimiter=",", quotechar="\"")
    for row in r_data:
        
        # GET PROPER FORMAT
        ( product_name, product_class_name, unit_cnt, unit, date_str, price_value ) = parsed2proper(row)
        if product_name == None:
            continue

        # GET ID
        product_id = get_product_id_by_name(product_name)
        assert(product_id != None)
        product_class_id = get_product_class_id_by_name(cur, product_id, product_class_name)

        # INSER PRICE INFO
        db_insert_price(cur, date_str, price_value, product_class_id)

    """
    for j in range(len(product[3])):
        
        price_value_default = random.randint(1000, 10000)
        price_value_delta_default = random.randint(0, math.floor(price_value_default / 10))
        price_value = price_value_default
        price_date = datetime.date.today()
        price_date_delta = datetime.timedelta(days=-1)
        
        for k in range(0, 366):
            db_insert_price(cur, price_date.strftime("%Y-%m-%d"), price_value, product_class_id)
            
            price_value += price_value_delta_default * random.uniform(-1.5, 2)
            price_date += price_date_delta
    """


    con.commit()