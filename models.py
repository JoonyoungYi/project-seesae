#-*- coding: utf-8 -*-
import datetime, random, math

class ProductModel:
	def __init__(self, product_id, product_type, product_name, img_url=None):
		self.id = product_id

		if (product_type == 1):
			self.type = '농산물'
		elif(product_type == 2):
			self.type = '수산물'
		elif(product_type == 3):
			self.type = '축산물'
		else:
			self.type=''

		self.name = product_name
		self.img_url = img_url

		self.change_day = int(math.floor((random.random() - 0.5) * 10))
		self.change_week = int(math.floor((random.random() - 0.5) * 10))
		self.change_month = int(math.floor((random.random() - 0.5)  * 10))

	def setSeason(self, season_start, season_end):

		d = datetime.date.today()
		current = d.month * 100 + d.day
		start = season_start.month * 100 + season_start.day
		end = season_end.month * 100 + season_end.day

		self.season_start = '%02d' % (season_start.month) + '-' + '%02d' % (season_start.day)
		self.season_end = '%02d' % (season_end.month) + '-' + '%02d' % (season_end.day)

		if ((start <= end and (start <= current <= end)) or ( start >= end and (current <= end or current >= start ))) :
			self.season = True
		else :
			self.season = False
		
class CommentModel:
	def __init__(self, comment_id, user_email, comment_content, timestamp):
		self.id = comment_id
		self.email = user_email
		self.content = comment_content
		self.timestamp = timestamp

class StoreModel:
	def __init__(self, store_name, latitude, longitude):
		self.name = store_name
		self.latitude = latitude
		self.longitude = longitude

class PriceChartModel:
	def __init__(self, product_class_id, product_class_name):
		self.label_color = "#AAAAAA"
		self.label_color_r = int("AA", 16)
		self.label_color_g = int("AA", 16)
		self.label_color_b = int("AA", 16)

		self.product_class_id = product_class_id
		self.product_class_name = product_class_name

	def setPrice_values(self, price_values):
		self.price_values = price_values

	def setLabel_color(self, label_color):
		self.label_color = label_color
		self.label_color_r = int(label_color[1:3], 16)
		self.label_color_g = int(label_color[3:5], 16)
		self.label_color_b = int(label_color[5:] , 16)
		print self.label_color_r
		print self.label_color_g
		print self.label_color_b

