import MySQLdb as mdb
from config import *

def db_connect():
    return mdb.connect(db_ip, db_username, db_password, db_name)

def db_init(con):

    with con:   
        cur = con.cursor()

        cur.execute("DROP TABLE IF EXISTS %s" % table_product )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s TINYINT, %s CHAR(50), %s CHAR(50), %s DATE, %s DATE, %s FLAOT, %s FLOAT )"\
                      % (table_product, column_product_id, column_product_type, column_product_name, column_product_img_url, \
                         column_product_season_start, column_product_season_end, column_producT_changeInDate, column_producT_changeInWeek, column_producT_changeInMonth  ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_product_class )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s CHAR(50), %s TINYINT, %s INT )"\
                      % (table_product_class, column_product_class_id, column_product_class_name, column_product_class_level, column_product_id))

        cur.execute("DROP TABLE IF EXISTS %s" % table_price )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s DATE, %s MEDIUMINT, %s INT )"\
                      % (table_price, column_price_id, column_price_date, column_price_value, column_product_class_id))

        cur.execute("DROP TABLE IF EXISTS %s" % table_user )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s CHAR(50), %s CHAR(50) )"\
                      % (table_user, column_user_id, column_user_email, column_user_password))

        cur.execute("DROP TABLE IF EXISTS %s" % table_comment )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s TEXT, %s TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, %s INT, %s INT )"\
                      % (table_comment, column_comment_id, column_comment_content, column_timestamp, column_user_id, column_product_id ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_favorite )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, %s INT, %s INT )"\
                      % (table_favorite, column_favorite_id, column_timestamp, column_user_id, column_product_id ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_hate )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, %s INT, %s INT )"\
                      % (table_hate, column_hate_id, column_timestamp, column_user_id, column_product_id ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_store )
        cur.execute("CREATE TABLE %s \
                      (%s INT PRIMARY KEY AUTO_INCREMENT, %s CHAR(50), %s FLOAT(9, 6), %s FLOAT(9, 6) )"\
                      % (table_store, column_store_id, column_store_name, column_store_latitude, column_store_longitude ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_product_store_relation )
        cur.execute("CREATE TABLE %s \
                      (%s INT, %s INT, PRIMARY KEY (%s, %s))" \
                      % (table_product_store_relation, column_product_id, column_store_id, column_product_id, column_store_id ))

        cur.execute("DROP TABLE IF EXISTS %s" % table_similar_product_relation )
        cur.execute("CREATE TABLE %s \
                      (%s INT, %s INT, PRIMARY KEY (%s, %s))"\
                      % (table_similar_product_relation, column_product_id, column_similar_product_id, column_product_id, column_similar_product_id ))        

def db_insert_user(cur, email, password):
    cur.execute("INSERT INTO %s (%s, %s) VALUES (\'%s\', \'%s\')" \
                  % (table_user, column_user_email, column_user_password, email, password))

def db_insert_product(cur, product_type, product_name, product_img_url, season_start, season_end):
    cur.execute("INSERT INTO %s (%s, %s, %s, %s, %s) VALUES (%d, \'%s\', \'%s\', \'%s\', \'%s\')" \
                  % (table_product, \
                     column_product_type, column_product_name, column_product_img_url, column_product_season_start, column_product_season_end, \
                     product_type, product_name, product_img_url, season_start, season_end))

def db_insert_product_class(cur, product_class_name, product_class_level, product_id):
    cur.execute("INSERT INTO %s (%s, %s, %s) VALUES (\'%s\', %d, %d)" \
                  % (table_product_class, \
                     column_product_class_name, column_product_class_level, column_product_id,\
                     product_class_name, product_class_level, product_id ))

def db_insert_price(cur, price_date, price_value, product_class_id):
    cur.execute("INSERT INTO %s (%s, %s, %s) VALUES (\'%s\', %d, %d)" \
                  % (table_price, \
                     column_price_date, column_price_value, column_product_class_id,\
                     price_date, price_value, product_class_id ))    

def db_insert_comment(cur, user_id, product_id, comment_content ):
    cur.execute("INSERT INTO %s (%s, %s, %s) VALUES (%d, %d, \'%s\' )" \
                  % (table_comment, column_user_id, column_product_id, column_comment_content, user_id, product_id, comment_content))

def db_insert_favorite(cur, user_id, product_id):
    cur.execute("INSERT INTO %s (%s, %s) VALUES (%d, %d)" \
                  % (table_favorite, column_user_id, column_product_id, user_id, product_id))

def db_insert_hate(cur, user_id, product_id):
    cur.execute("INSERT INTO %s (%s, %s) VALUES (%d, %d)" \
                  % (table_hate, column_user_id, column_product_id, user_id, product_id))

def db_insert_store(cur, store_name, store_latitude, store_longitude):
    cur.execute("INSERT INTO %s (%s, %s, %s) VALUES (\'%s\', %f, %f )" \
                  % (table_store, column_store_name, column_store_latitude, column_store_longitude, \
                     store_name, store_latitude, store_longitude))  

def db_insert_product_store_relation(cur, product_id, store_id):
    cur.execute("SELECT * FROM %s WHERE %s=%d and %s=%d LIMIT 1" \
               % (table_product_store_relation, column_product_id, product_id, column_store_id, store_id))
    rows = cur.fetchall()

    if len(rows) == 0:
        cur.execute("INSERT INTO %s (%s, %s) VALUES ( %d, %d )" \
                  % (table_product_store_relation, column_product_id, column_store_id, product_id, store_id ))

def db_insert_similar_product_relation(cur, product_id, similar_product_id):
    cur.execute("SELECT * FROM %s WHERE %s=%d and %s=%d LIMIT 1" \
               % (table_similar_product_relation, column_product_id, product_id, column_similar_product_id, similar_product_id))
    rows = cur.fetchall()

    if len(rows) == 0:
        cur.execute("INSERT INTO %s (%s, %s) VALUES ( %d, %d )" \
                  % (table_similar_product_relation, column_product_id, column_similar_product_id, product_id, similar_product_id))


