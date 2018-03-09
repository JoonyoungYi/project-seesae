#-*- coding: utf-8 -*-
from flask import Flask, g, render_template, redirect, request, session, url_for
from db import db_connect, db_insert_favorite, db_insert_hate, db_insert_comment
from config import *
from models import *
import datetime, math, itertools
import sys, random

# -----------------------------------------------------------------------------
# FOR ENCODING
# -----------------------------------------------------------------------------
reload(sys)
sys.setdefaultencoding('utf-8')

# -----------------------------------------------------------------------------
# BASE AND MAIN
# -----------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(__name__)

"""
BASE REQUEST
"""
@app.before_request
def before_request():
    g.db = db_connect()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None :
        db.close()

# -----------------------------------------------------------------------------
# SECTION FOR MAIN PAGE
# -----------------------------------------------------------------------------
@app.route('/')
def show_main():
    return make_main('all')

@app.route('/agricultural')
def show_main_agiricultural():
    return make_main('agricultural')

@app.route('/fishery')
def show_main_fishery():
    return make_main('fishery')

@app.route('/livestock')
def show_main_livestock():
    return make_main('livestock')

def make_main(product_type):

    if not is_logged_in():
        return redirect(url_for('login'))

    # user_id
    if 'user_id' in session :
        user_id = session['user_id']

    cur = g.db.cursor()
    for_display = None
    if product_type == 'agricultural':
        cur.execute('SELECT * FROM %s WHERE %s=1' % (table_product, column_product_type))
        for_display = { "wp" : "wallpaper-agriculture", "title":"AGRICULTURAL"}
    elif product_type == 'fishery':
        cur.execute('SELECT * FROM %s WHERE %s=2' % (table_product, column_product_type))
        for_display = { "wp" : "wallpaper-fishery", "title":"FISHERY" }
    elif product_type == 'livestock':
        cur.execute('SELECT * FROM %s WHERE %s=3' % (table_product, column_product_type))    
        for_display = { "wp" : "wallpaper-livestock", "title":"LIVESTOCK" }
    else :
        cur.execute('SELECT * FROM %s' % (table_product))
        for_display = { "wp" : "wallpaper-agriculture", "title":"SEE-SAE" }
    rows = cur.fetchall()

    products = []
    for row in rows:
        product = ProductModel(row[0], row[1], row[2], row[3])
        if row[4] == None or row[5] == None:    
            continue
        product.setSeason(row[4], row[5])
        products.append(product)

    random.shuffle(products)
    ###
    cur.execute('SELECT * FROM %s WHERE %s=%d' % (table_hate,  column_user_id, user_id)) 

    ### 
    cur.execute('SELECT * FROM %s WHERE %s=%d' % (table_hate,  column_user_id, user_id)) 
    rows = cur.fetchall()
    id_hates = []
    for row in rows:   
        id_hates.append(rows[3])

    new_products = []
    for product in products:
        if not product.id in id_hates:
            new_products.append(product)

    products = new_products
    ###   

    return render_template('main.html', product_type=product_type, products=products, for_display=for_display)

"""
SECTION FOR DETAIL
"""
@app.route('/<int:product_id>/')
def show_detail(product_id):

    if not is_logged_in():
        return redirect(url_for('login'))

    cur = g.db.cursor()

    # user_id
    if 'user_id' in session :
        user_id = session['user_id']
    
    # PRODUCT!!!! and SEASON!!!
    cur.execute('SELECT * FROM %s WHERE %s=%d LIMIT 1' % (table_product, column_product_id, product_id))
    row = cur.fetchall()[0]
    product = ProductModel(row[0], row[1], row[2], row[3])
    if row[4] == None or row[5] == None:
        return redirect(url_for('show_main'))
    product.setSeason(row[4], row[5])

    # PRICES
    cur.execute('SELECT * FROM %s WHERE %s=%d' % (table_product_class, column_product_id, product_id))
    price_charts_day = []
    price_charts_week = []
    price_charts_month = []
    rows = cur.fetchall()
    for row in rows:
        price_chart_day = PriceChartModel(row[0], row[1])
        price_charts_day.append(price_chart_day)
        price_chart_week = PriceChartModel(row[0], row[1])
        price_charts_week.append(price_chart_week)
        price_chart_month = PriceChartModel(row[0], row[1])
        price_charts_month.append(price_chart_month)

    price_date_end = datetime.date.today()
    price_date_end_str = price_date_end.strftime("%Y-%m-%d")
    price_date_start = price_date_end + datetime.timedelta(days=-7)
    price_date_start_str = price_date_start.strftime("%Y-%m-%d")

    colors = ['#FF6F00', '#FF8F00', '#FFA000', '#FFB300', '#FFC107', '#FFCA28']
    def setLabelColors(price_charts):
        price_charts.sort(key=lambda x: (sum( x.price_values ) / len(x.price_values)) , reverse=True)
        for i, price_chart in enumerate(price_charts):
            price_chart.setLabel_color(colors[ int(math.floor( len(colors) * i / len(price_charts) )) ])
        return price_charts

    for price_chart in price_charts_day:
        cur.execute('SELECT ROUND(AVG(%s)), DAY(%s) FROM %s WHERE %s=%d and %s BETWEEN \'%s\' and \'%s\' \
                     GROUP BY %s ORDER BY %s ASC' \
                   % (column_price_value, column_price_date, table_price, \
                      column_product_class_id, price_chart.product_class_id, column_price_date, \
                      price_date_start_str, price_date_end_str, \
                      column_price_date, column_price_date))
        rows = cur.fetchall()
        price_values = []

        old_value = None
        for row in rows:
            
            if old_value != None:
                if old_value + 1 != int(row[1]):
                    for i in range( 1, int(row[1]) - old_value) :
                        price_values.append(0)
            old_value = int(row[1])

            price_values.append(int(row[0]))
        
        if (len(price_values) <= 8 ):
            for i in range( 8 - len(price_values)):
                price_values.append(0)

        print len (price_values)
        assert( len (price_values) == 8 )
        price_chart.price_values = price_values
    
    price_charts_day = setLabelColors(price_charts_day)

    price_date_start = price_date_end + datetime.timedelta(weeks=-12)
    price_date_start_str = price_date_start.strftime("%Y-%m-%d")
    for price_chart in price_charts_week:
        cur.execute('SELECT ROUND(AVG(%s)), WEEK(%s) FROM %s WHERE %s=%d and %s > 0 and %s BETWEEN \'%s\' and \'%s\' \
                     GROUP BY CONCAT(YEAR(%s), \'/\', WEEK(%s)) ORDER BY %s ASC' \
                   % (column_price_value, column_price_date, table_price, \
                      column_product_class_id, price_chart.product_class_id, column_price_value, column_price_date, \
                      price_date_start_str, price_date_end_str,\
                      column_price_date, column_price_date, column_price_date))
        rows = cur.fetchall()
        price_values = []

        old_value = None
        for row in rows:
            
            if old_value != None:
                if old_value + 1 != int(row[1]):
                    for i in range( 1, int(row[1]) - old_value) :
                        price_values.append(0)
            old_value = int(row[1])

            price_values.append(int(row[0]))
        
        if (len(price_values) < 13 ):
            for i in range( 13 - len(price_values)):
                price_values.append(0)

        print '>> ' + str(len (price_values))
        assert( len (price_values) == 13 )
        price_chart.price_values = price_values

    price_charts_day = setLabelColors(price_charts_week)

    price_date_start = price_date_end + datetime.timedelta(days=-365)
    price_date_start_str = price_date_start.strftime("%Y-%m-%d")
    for price_chart in price_charts_month:
        cur.execute('SELECT ROUND(AVG(%s)), MONTH(%s) FROM %s WHERE %s=%d and %s BETWEEN \'%s\' and \'%s\' \
                     GROUP BY CONCAT(YEAR(%s), \'/\', MONTH(%s)) ORDER BY %s ASC' \
                   % (column_price_value, column_price_date, table_price, \
                      column_product_class_id, price_chart.product_class_id, column_price_date, \
                      price_date_start_str, price_date_end_str,\
                      column_price_date, column_price_date, column_price_date))
        rows = cur.fetchall()
        price_values = []
        
        old_value = None
        for row in rows:
            
            if old_value != None:
                if old_value + 1 != int(row[1]):
                    for i in range( 1, int(row[1]) - old_value) :
                        price_values.append(0)
            old_value = int(row[1])

            price_values.append(int(row[0]))
        
        if (len(price_values) < 13 ):
            for i in range( 13 - len(price_values)):
                price_values.append(0)

        print '>> ' + str(len (price_values))

        price_chart.price_values = price_values

    price_charts_day = setLabelColors(price_charts_month)

    # SIMILAR PRODUCTS!!!
    cur.execute('SELECT %s.%s, %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s.%s=%d' \
               % (table_product, column_product_id, \
                  table_product, column_product_type, \
                  table_product, column_product_name, \
                  table_product, column_product_img_url, \
                  table_similar_product_relation, table_product, \
                  table_similar_product_relation, column_similar_product_id, table_product, column_product_id, \
                  table_similar_product_relation, column_product_id, product_id))
    rows = cur.fetchall()
    similar_products = []
    for row in rows:
        similar_product = ProductModel(row[0], row[1], row[2], row[3])
        similar_products.append(similar_product)    

    # LIKE/HATE INFORMATION
    cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
               % ( table_favorite, column_product_id, product_id, column_user_id, user_id ))
    rows = cur.fetchall()
    for row in rows:
        print row
    dLike = {}
    if len(rows) == 1:
        dLike['like'] = 'btn-success'
        print dLike['like']
    else:
        dLike['like'] = ''
    cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
               % ( table_hate, column_product_id, product_id, column_user_id, user_id ))
    rows = cur.fetchall()
    for row in rows:
        print row
    if len(rows) == 1:
        dLike['hate'] = 'btn-danger'
        print dLike['hate']
    else :
        dLike['hate'] = ''

    # STORES!!!!
    cur.execute('SELECT %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s.%s=%d LIMIT 4' \
               % (table_store, column_store_name, \
                  table_store, column_store_latitude, \
                  table_store, column_store_longitude, \
                  table_product_store_relation, table_store, \
                  table_product_store_relation, column_store_id, table_store, column_store_id, \
                  table_product_store_relation, column_product_id, product_id))
    rows = cur.fetchall()
    stores = []
    for row in rows:
        store = StoreModel(row[0], row[1], row[2])
        stores.append(store)

    # COMMENTS!!!
    cur.execute('SELECT %s.%s, %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s=%d ORDER BY %s.%s DESC' \
               % (table_comment, column_comment_id, \
                  table_comment, column_comment_content, \
                  table_user, column_user_email, table_comment, column_timestamp, \
                  table_comment, table_user, \
                  table_comment, column_user_id, table_user, column_user_id, column_product_id, product_id, table_comment, column_timestamp))
    rows = cur.fetchall()
    comments = []
    for row in rows:
        comment = CommentModel(row[0], row[2], row[1], row[3])
        comments.append(comment)

    return render_template('detail.html', \
                            product=product, \
                            price_charts_day=price_charts_day, price_charts_week=price_charts_week, price_charts_month=price_charts_month, \
                            similar_products=similar_products, stores=stores, comments=comments, dLike=dLike)

# -----------------------------------------------------------------------------
# LIKE HATE BUTTON
# -----------------------------------------------------------------------------

@app.route('/toggle/like/<int:product_id>/')
def toggle_like(product_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    cur = g.db.cursor()

    # user_id
    if 'user_id' in session :
        user_id = session['user_id']
    
    # LIKE/HATE INFORMATION
    cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
               % ( table_favorite, column_product_id, product_id, column_user_id, user_id ))
    rows = cur.fetchall()
    if len(rows) == 1:
        cur.execute('DELETE FROM %s WHERE %s=%d' \
               % ( table_favorite, column_favorite_id, rows[0][0]))
    else :
        db_insert_favorite(cur, user_id, product_id)

        cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
                % ( table_hate, column_product_id, product_id, column_user_id, user_id ))
        rows = cur.fetchall()
        if len(rows) == 1:
            cur.execute('DELETE FROM %s WHERE %s=%d' \
                    % ( table_hate, column_hate_id, rows[0][0]))         
    g.db.commit()

    return redirect(url_for('show_detail', product_id=product_id))

@app.route('/toggle/hate/<int:product_id>/')
def toggle_hate(product_id):
    if not is_logged_in():
        return redirect(url_for('login'))

    cur = g.db.cursor()

    # user_id
    if 'user_id' in session :
        user_id = session['user_id']
    
    # LIKE/HATE INFORMATION
    cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
               % ( table_hate, column_product_id, product_id, column_user_id, user_id ))
    rows = cur.fetchall()
    if len(rows) == 1:
        cur.execute('DELETE FROM %s WHERE %s=%d' \
               % ( table_hate, column_hate_id, rows[0][0]))
    else :
        db_insert_hate(cur, user_id, product_id)

        cur.execute('SELECT * FROM %s WHERE %s=%d and %s=%d' \
                % ( table_favorite, column_product_id, product_id, column_user_id, user_id ))
        rows = cur.fetchall()
        if len(rows) == 1:
            cur.execute('DELETE FROM %s WHERE %s=%d' \
                    % ( table_favorite, column_favorite_id, rows[0][0]))         
    g.db.commit()

    return redirect(url_for('show_detail', product_id=product_id))

# -----------------------------------------------------------------------------
# COMMENT ADD
# -----------------------------------------------------------------------------
@app.route('/add/comment/<int:product_id>', methods=['POST'])
def add_comment(product_id):
    
    if request.method == 'POST':

        # user_id
        if 'user_id' in session :
            user_id = session['user_id']
        
        cur = g.db.cursor()
        print (user_id, product_id, request.form['content'])
        db_insert_comment(cur, user_id, product_id, request.form['content'].encode('utf-8'))

        g.db.commit()

    return redirect(url_for('show_detail', product_id=product_id))

"""
SECTION FOR MY PAGE
"""
@app.route('/profile/')
def show_profile():

    if not is_logged_in():
        return redirect(url_for('login'))

    if 'username' in session:
        pass

    # user_id
    if 'user_id' in session :
        user_id = session['user_id']

    # 
    cur = g.db.cursor()
    cur.execute('SELECT %s.%s, %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s.%s=%d' \
              % (table_product, column_product_id, \
                 table_product, column_product_type, \
                 table_product, column_product_name, \
                 table_product, column_product_img_url, \
                 table_favorite, table_product, \
                 table_product, column_product_id, \
                 table_favorite, column_product_id, \
                 table_favorite, column_user_id, user_id)) 
    rows = cur.fetchall()
    favorites = []
    for row in rows:
        product = ProductModel(row[0], row[1], row[2], row[3])
        favorites.append(product)

    # COMMENTS!!!
    product_id = 1
    cur.execute('SELECT %s.%s, %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s.%s=%d' \
               % (table_comment, column_comment_id, \
                  table_comment, column_comment_content, \
                  table_product, column_product_name, \
                  table_comment, column_timestamp, \
                  table_comment, table_product, \
                  table_comment, column_product_id, table_product, column_product_id, table_comment, column_user_id, user_id))
    rows = cur.fetchall()
    comments = []
    for row in rows:
        comment = CommentModel(row[0], row[2], row[1], row[3])
        comments.append(comment)

    # 
    cur.execute('SELECT %s.%s, %s.%s, %s.%s, %s.%s FROM %s LEFT JOIN %s ON %s.%s=%s.%s WHERE %s.%s=%d' \
          % (table_product, column_product_id, \
             table_product, column_product_type, \
             table_product, column_product_name, \
             table_product, column_product_img_url, \
             table_hate, table_product, \
             table_product, column_product_id, \
             table_hate, column_product_id, \
             table_hate, column_user_id, user_id)) 

    rows = cur.fetchall()
    hates = []
    for row in rows:
        product = ProductModel(row[0], row[1], row[2], row[3])
        hates.append(product)

    # show the user profile for that user
    return render_template('profile.html', favorites=favorites, hates=hates, comments=comments )

"""
SECTION FOR LOGIN AND JOIN
"""
def is_logged_in():

    if 'logged_in' in session:
        return True
    else:
        return False

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':

        try :
          request.form['login']
        except:
          return redirect(url_for('join'))

        cur = g.db.cursor()
        cur.execute('SELECT * FROM %s WHERE %s=\'%s\' and %s=\'%s\'' \
               % (table_user, \
                  column_user_email, request.form['email'], \
                  column_user_password, request.form['password']))
        rows = cur.fetchall()

        if len(rows) == 1:
            session['logged_in'] = True
            session['username'] = request.form['email']
            session['user_id'] = rows[0][0]
            # flash('You were logged in')
            return redirect(url_for('show_main'))

        error='Check your email and password'

    return render_template('login.html', error=error)

@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('user_id', None)
    #flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/join/')
def join():
    error=None
    return render_template('join.html', error=error)

"""
SECTION FOR RUNNING APP
"""
if __name__ == '__main__':
    app.run(debug=True)
