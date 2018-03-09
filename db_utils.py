# -*- coding:utf-8 -*-
def parsed2proper(parsed_row):

	try:
		price = int(parsed_row[2])
		date_str = parsed_row[1]
		category_raw = parsed_row[0]
		product_name = ''
		product_class_name = category_raw
		unit_cnt = str(1)
		unit = ''

		if '포기' in category_raw:
			product_name = '배추'
			product_class_name = category_raw[0:category_raw.index("품")].replace("전체(", "")
			unit = '포기'
		if '느타리버섯' in category_raw:
			product_name = '느타리버섯'
			product_class_name = category_raw[0:category_raw.index("품")].replace("느타리버섯(", "")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("g", "")
			unit = 'g'
		elif '후지' in category_raw:
			product_name = '사과'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("개", "")
			unit = '개'
		elif '신고' in category_raw:
			product_name = '배'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("개", "")
			unit = '개'
		elif '감귤' in category_raw :
			product_name = '감귤'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/").replace("감귤/", "")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("개", "")
			unit = '개'	
		elif ('수입' in category_raw) and ('품' in category_raw ):
			product_name = '바나나'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("g", "")
			unit = 'g'
		elif '발렌시아' in category_raw:
			product_name = '오렌지'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("개", "")
			unit = '개'
		elif '딸기' in category_raw :
			product_name = '딸기'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/").replace("딸기/", "")
			unit_cnt = category_raw[(category_raw.index(":")+1):].replace("g", "")
			unit = 'g'
		elif '수박' in category_raw:
			product_name = '수박'
			product_class_name = category_raw[0:category_raw.index("품")].replace("(", "/").replace("수박/", "")
			unit = "개"

		elif '굴' in category_raw:
			product_name = '굴'
			product_class_name = category_raw.replace('굴', '')
			
			# delivery
			delivery = ''
			if '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'	
			else:
				assert(False)

			# method
			method = ''
			if '바위:' in product_class_name:
				product_class_name = product_class_name.replace("바위:", "")
				method = '바위'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'

			# region
			if "(" in product_class_name or ")" in product_class_name :
				return ( None, None, None, None, None, None )
			product_class_name = '국내'

			# concat all information
			product_class_name = method + '/'+delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size


		elif '꼬막' in category_raw:
			product_name = '꼬막'
			product_class_name = category_raw.replace('꼬막', '')

			# delivery
			delivery = ''
			if '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)
			
			# method
			method = ''
			if '돌:' in product_class_name:
				product_class_name = product_class_name.replace("돌:", "")
				method = '돌'
			elif '새:' in product_class_name:
				product_class_name = product_class_name.replace("새:", "")
				method = '새'
			elif '참:' in product_class_name:
				product_class_name = product_class_name.replace("참:", "")
				method = '참'
			else:
				assert(False)

			# size
			size = ''
			if '(중소)' in product_class_name:
				product_class_name = product_class_name.replace('(중소)', '')
				size = '중소'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'

			# region
			assert( "(" not in product_class_name and ")" not in product_class_name)
			if '중국' not in product_class_name and '일본' not in product_class_name and '태국' not in product_class_name:
				product_class_name = '국내'

			# concat all information
			product_class_name = method + '/'+delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size

		elif '넙치' in category_raw:
			product_name = '넙치'

			product_class_name = category_raw.replace('넙치:', '').replace('부산(기장)', '국내')

			# unit 
			if '미)' in product_class_name:
				unit = '미'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(")")) + 1):product_class_name.index("미)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')

			# delivery
			delivery = ''
			if '가공' in product_class_name:
				product_class_name = product_class_name.replace("(가공)", "")
				delivery = '가공'
			elif '냉' in product_class_name:
				product_class_name = product_class_name.replace("(냉)", "")
				delivery = '냉'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'
			elif '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대중)' in product_class_name:
				product_class_name = product_class_name.replace('(대중)', '')
				size = '대중'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'
			elif '(중소)' in product_class_name:
				product_class_name = product_class_name.replace('(중소)', '')
				size = '중소'
			elif '(소소)' in product_class_name:
				product_class_name = product_class_name.replace('(소소)', '')
				size = '소소'
			elif '(2L)' in product_class_name:
				product_class_name = product_class_name.replace('(2L)', '')
				size = '특대'
			elif '(L)' in product_class_name:
				product_class_name = product_class_name.replace('(L)', '')
				size = '대'
			elif '(M)' in product_class_name:
				product_class_name = product_class_name.replace('(M)', '')
				size = '중'
			elif '(M2)' in product_class_name:
				product_class_name = product_class_name.replace('(M2)', '')
				size = '중소'
			elif '(S)' in product_class_name:
				product_class_name = product_class_name.replace('(S)', '')
				size = '소'
			elif '(2S)' in product_class_name:
				product_class_name = product_class_name.replace('(2S)', '')
				size = '소소'

			# region
			if "(" in product_class_name or ")" in product_class_name :
				return ( None, None, None, None, None, None )
			product_class_name = '국내'

			# concat all information
			product_class_name = delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size

		elif '낙지' in category_raw:
			product_name = '낙지'
			product_class_name = category_raw.replace('낙지:', '').replace('베트남', '수입')

			# unit 
			if '미)' in product_class_name:
				unit = '미'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(")")) + 1):product_class_name.index("미)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')

			# delivery
			delivery = ''
			if '가공' in product_class_name:
				product_class_name = product_class_name.replace("(가공)", "")
				delivery = '가공'
			elif '냉' in product_class_name:
				product_class_name = product_class_name.replace("(냉)", "")
				delivery = '냉'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'
			elif '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'
			elif '(중소)' in product_class_name:
				product_class_name = product_class_name.replace('(중소)', '')
				size = '중소'
			elif '(소소)' in product_class_name:
				product_class_name = product_class_name.replace('(소소)', '')
				size = '소소'
			elif '(2L)' in product_class_name:
				product_class_name = product_class_name.replace('(2L)', '')
				size = '특대'
			elif '(L)' in product_class_name:
				product_class_name = product_class_name.replace('(L)', '')
				size = '대'
			elif '(M)' in product_class_name:
				product_class_name = product_class_name.replace('(M)', '')
				size = '중'
			elif '(M2)' in product_class_name:
				product_class_name = product_class_name.replace('(M2)', '')
				size = '중소'
			elif '(S)' in product_class_name:
				product_class_name = product_class_name.replace('(S)', '')
				size = '소'
			elif '(2S)' in product_class_name:
				product_class_name = product_class_name.replace('(2S)', '')
				size = '소소'

			# region
			if "(" in product_class_name or ")" in product_class_name :
				return ( None, None, None, None, None, None )

			if '중국' not in product_class_name and '수입' not in product_class_name:
				product_class_name = '국내'

			# concat all information
			product_class_name = method + '/'+delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size


		elif '바지락' in category_raw:
			product_name = '바지락'
			
			# preprocessing
			product_class_name = category_raw.replace('바지락', '').replace('기타(국내)', '국내').replace('기타(수입)', '수입')

			# unit 
			if '봉)' in product_class_name:
				unit = '봉'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(":")) + 1):product_class_name.index("봉)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')
			elif '통)' in product_class_name:
				unit = '통'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(":")) + 1):product_class_name.index("통)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')
				unit = '봉'
			elif '미)' in product_class_name:
				unit = '미'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(":")) + 1):product_class_name.index("미)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')
				unit = '봉'

			# delivery
			delivery = ''
			if '가공' in product_class_name:
				product_class_name = product_class_name.replace("(가공)", "")
				delivery = '가공'
			elif '냉' in product_class_name:
				product_class_name = product_class_name.replace("(냉)", "")
				delivery = '냉'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'
			elif '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)

			# method
			method = ''
			if '겉' in product_class_name:
				product_class_name = product_class_name.replace("겉:", "")
				method = '겉'
			elif '깐' in product_class_name:
				product_class_name = product_class_name.replace("깐:", "")
				method = '깐'
			elif '물' in product_class_name:
				product_class_name = product_class_name.replace("물:", "")
				method = '물'
			elif '봉' in product_class_name:
				product_class_name = product_class_name.replace("봉:", "")
				method = '봉'
			elif '칼' in product_class_name:
				product_class_name = product_class_name.replace("칼:", "")
				method = '칼'
			elif '토' in product_class_name:
				product_class_name = product_class_name.replace("토:", "")
				method = '토'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'

			# region
			assert( "(" not in product_class_name and ")" not in product_class_name)
			if '중국' not in product_class_name and '수입' not in product_class_name:
				product_class_name = '국내'

			# concat all information
			product_class_name = method + '/'+delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size

		elif '오징어' in category_raw:
			product_name = '오징어'
			product_class_name = category_raw.replace('오징어:', '')\
					.replace('(원양)뉴질랜드', '원양').replace('(원양)포클랜드', '원양').replace('기타(원양)', '원양')\
					.replace('기타(수입)', '수입').replace('뉴질랜드', '수입').replace('중국', '수입').replace('대만','수입')\
					.replace('서남부대서양', '수입').replace('칠레', '수입').replace('포르투갈', '수입')\
					.replace('기타(국내)', '국내').replace('부산(기장)', '국내')

			# unit 
			if '미)' in product_class_name:
				unit = '미'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(")")) + 1):product_class_name.index("미)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')
				
			# delivery
			delivery = ''
			if '가공' in product_class_name:
				product_class_name = product_class_name.replace("(가공)", "")
				delivery = '가공'
			elif '냉' in product_class_name:
				product_class_name = product_class_name.replace("(냉)", "")
				delivery = '냉'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'
			elif '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'
			elif '(중소)' in product_class_name:
				product_class_name = product_class_name.replace('(중소)', '')
				size = '중소'
			elif '(소소)' in product_class_name:
				product_class_name = product_class_name.replace('(소소)', '')
				size = '소소'
			elif '(2L)' in product_class_name:
				product_class_name = product_class_name.replace('(2L)', '')
				size = '특대'
			elif '(L)' in product_class_name:
				product_class_name = product_class_name.replace('(L)', '')
				size = '대'
			elif '(M)' in product_class_name:
				product_class_name = product_class_name.replace('(M)', '')
				size = '중'
			elif '(M2)' in product_class_name:
				product_class_name = product_class_name.replace('(M2)', '')
				size = '중소'
			elif '(S)' in product_class_name:
				product_class_name = product_class_name.replace('(S)', '')
				size = '소'
			elif '(2S)' in product_class_name:
				product_class_name = product_class_name.replace('(2S)', '')
				size = '소소'
			
			# region
			if "(" in product_class_name or ")" in product_class_name :
				return ( None, None, None, None, None, None )
			if '원양' not in product_class_name and '수입' not in product_class_name:
				product_class_name = '국내'

			# concat all information
			product_class_name = delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size

		elif '조기' in category_raw or '부세' in category_raw:
			product_name = '조기'
			
			# preprocessing
			product_class_name = category_raw.replace('조기', '')\
					.replace('부산(기장)', '국내').replace('기타(국내)', '국내')\
					.replace('(원양)인도네시아', '수입').replace('기타(원양)', '수입')\
					.replace('기타(수입)','수입').replace('러시아', '수입').replace('중국', '수입')
			
			# unit 
			if '미)' in product_class_name:
				unit = '미'
				unit_cnt = product_class_name[(product_class_name.index("(", product_class_name.index(")")) + 1):product_class_name.index("미)")]
				product_class_name = product_class_name.replace('('+unit_cnt+unit+')', '')


			# delivery
			delivery = ''
			if '가공' in product_class_name:
				product_class_name = product_class_name.replace("(가공)", "")
				delivery = '가공'
			elif '냉' in product_class_name:
				product_class_name = product_class_name.replace("(냉)", "")
				delivery = '냉'
			elif '선' in product_class_name:
				product_class_name = product_class_name.replace("(선)", "")
				delivery = '선'
			elif '활' in product_class_name:
				product_class_name = product_class_name.replace("(활)", "")
				delivery = '활'
			else:
				assert(False)

			# method
			method = ''
			if '참' in product_class_name:
				product_class_name = product_class_name.replace("참:", "")
				method = '참'
			elif '백' in product_class_name:
				product_class_name = product_class_name.replace("백:", "")
				method = '백'
			elif '부세' in product_class_name:
				product_class_name = product_class_name.replace("부세:", "")
				method = '부세'
			elif '수' in product_class_name:
				product_class_name = product_class_name.replace("수:", "")
				method = '수'
			else:
				assert(False)

			# size
			size = ''
			if '(특대)' in product_class_name:
				product_class_name = product_class_name.replace('(특대)', '')
				size = '특대'
			elif '(대)' in product_class_name:
				product_class_name = product_class_name.replace('(대)', '')
				size = '대'
			elif '(중)' in product_class_name:
				product_class_name = product_class_name.replace('(중)', '')
				size = '중'
			elif '(소)' in product_class_name:
				product_class_name = product_class_name.replace('(소)', '')
				size = '소'
			elif '(중소)' in product_class_name:
				product_class_name = product_class_name.replace('(중소)', '')
				size = '중소'
			elif '(소소)' in product_class_name:
				product_class_name = product_class_name.replace('(소소)', '')
				size = '소소'
			elif '(2L)' in product_class_name:
				product_class_name = product_class_name.replace('(2L)', '')
				size = '특대'
			elif '(L)' in product_class_name:
				product_class_name = product_class_name.replace('(L)', '')
				size = '대'
			elif '(M)' in product_class_name:
				product_class_name = product_class_name.replace('(M)', '')
				size = '중'
			elif '(M2)' in product_class_name:
				product_class_name = product_class_name.replace('(M2)', '')
				size = '중소'
			elif '(S)' in product_class_name:
				product_class_name = product_class_name.replace('(S)', '')
				size = '소'
			elif '(2S)' in product_class_name:
				product_class_name = product_class_name.replace('(2S)', '')
				size = '소소'

			# region
			if "(" in product_class_name or ")" in product_class_name :
				return ( None, None, None, None, None, None )
			if '원양' not in product_class_name and '수입' not in product_class_name:
				product_class_name = '국내'

			# concat all information
			product_class_name = method + '/'+delivery +'/'+product_class_name
			if size != '':
				product_class_name += '/' + size

		elif '돈육' in category_raw:
			product_name = '돼지고기'
			product_class_name = category_raw.replace("돈육:", "")
		elif '안심' in category_raw :
			product_name = '안심(소고기)'
			product_class_name = category_raw.replace("안심(", "").replace(":", "/").replace(")", "")
		elif '등심' in category_raw :
			product_name = '등심(소고기)'
			product_class_name = category_raw.replace("등심(", "").replace(":", "/").replace(")", "")
		elif '사골' in category_raw:
			product_name = '사골(소고기)'
			product_class_name = category_raw.replace("사골(", "").replace(":", "/").replace(")", "")
		elif '양지' in category_raw:
			product_name = '양지(소고기)'
			product_class_name = category_raw.replace("양지(", "").replace(":", "/").replace(")", "")
		elif '사태' in category_raw:
			product_name = '사태(소고기)'
			product_class_name = category_raw.replace("사태(", "").replace(":", "/").replace(")", "")
		else :
			return ( None, None, None, None, None, None )

		return ( product_name, product_class_name, unit_cnt, unit, date_str, int(price) )
	except:
		return ( None, None, None, None, None, None )
