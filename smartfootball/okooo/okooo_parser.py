# -*- coding:utf-8 -*-
import requests
import lxml.html 
from datetime import datetime,timedelta
import time
from threading import Timer 

from utility import *
from setting import *
from okooo.okooo_setting import *
from okooo.okooo_match import *

# sid 20150501
# seq 001
# mid 20150501001
def parse_page_jc(dt):
	# http://www.okooo.com/livecenter/jingcai/?date=2015-05-26
	url = get_url_jc(dt)
	r = requests.get(url)
	text = r.text
	if r.encoding != "utf-8":
		print "[Warning] page is not utf-8 encoding, so encode it."
		text = r.text.encode(r.encoding)
	html = lxml.html.document_fromstring(text)

	path = '//*[@id="livescore_table"]/table'
	table_list = html.xpath(path)
	if len(table_list) == 0:
		print "[Warning] no table results..."
		return
	table = table_list[0]

	match_list = []
	for tr in table.getchildren():
		if tr.attrib.has_key('matchid'):
			td_list = tr.getchildren()
			seq = unicode(td_list[0].find('span').text)
			league = unicode(td_list[1].find('a').text)
			time = td_list[2].text
			# 05-26 18:00
			str_match_time = str(dt.year)+"-"+time
			match_time = str_to_dt(str_match_time)
			match_status = unicode(td_list[3].find('span').text)
			home_name = unicode(td_list[4].find('a').text)
			score_list = td_list[5].find('a').findall('b')
			home_full_score = score_list[0].text
			away_full_score = score_list[2].text
			away_name = unicode(td_list[6].find('a').text)
			half_score = unicode(td_list[7].find('span').text)
			# 1-3,  -
			home_half_score = None
			away_half_score = None
			if len(half_score) > 1:
				parts = half_score.split(u'-')
				home_half_score = parts[0]
				away_half_score = parts[1]

			match_id = dt.strftime("%Y%m%d")+seq
			pid = okooo_id = unicode(tr.attrib['matchid'])
			# match result
			match_result_obj = MatchResult(match_id,home_full_score,away_full_score,home_half_score,away_half_score)
			# use jingcai to collect odds
			bookmaker_id = 2
			# odd collection
			odd_collection = parse_page_odds_change(match_id,okooo_id,bookmaker_id)

			# match info
			okooo_match_info = OkoooMatchInfo(match_id,league,home_name,away_name,match_time,pid,match_status,odd_collection,match_result_obj)
			
			print "="*80
			match_list.append(okooo_match_info)
	return match_list

def parse_page_odds_change(match_id,okooo_id,bookmaker_id):
	odd_collection = OddCollection(match_id,okooo_id,bookmaker_id)
	url = get_url_odds_change(okooo_id,bookmaker_id)
	r = requests.get(url)
	text = r.text
	if r.encoding != "utf-8":
		print "[Warning] page is not utf-8 encoding, so encode it."
		text = r.text.encode(r.encoding)
	html = lxml.html.document_fromstring(text)

	path = '/html/body/div[1]/table'
	table_list = html.xpath(path)
	if len(table_list) == 0:
		print "[Warning] no table results..."
		return
	table = table_list[0]
	tr_list = table.getchildren()
	"""
	{'class': 'tableh'}
	{'class': 'titlebg'}
	{} ----------------------------------
	{'class': 'titlebg'}
	{'class': ''} -----------------------
	{'class': 'sjbg01'}------------------
	{'class': ''}------------------------
	"""
	# 2,4-N
	new_tr_list = []
	new_tr_list.append(tr_list[2])
	count = len(tr_list)
	for i in range(4,count):
		new_tr_list.append(tr_list[i])
	#print len(new_tr_list)
	"""
	<tr>
        <td class="noborder bright">2015/05/31 21:26(实时)</td>
        <td class="bright">赛前5小时18分</td>
        <td>1.40</td>
        <td>4.40</td>
        <td class="bright">5.50</td>
        <td>63.58</td>
        <td>20.23</td>
        <td class="bright">16.18</td>
        <td><span class="bluetxt">0.92↓</span></td>
        <td><span class="redtxt">0.89↑</span></td>
        <td class="bright"><span class="redtxt">0.76↑</span></td>
        <td class="bright">0.89</td>
        </tr>
	"""
	for tr in new_tr_list:
		td_list = tr.getchildren()
		str_time = td_list[0].text.split('(')[0]
		# 2015/05/31 21:26
		time = datetime.strptime(str_time,"%Y/%m/%d %H:%M")
		update_time = unicode(td_list[1].text)
		odd_a = pts(td_list[2])
		odd_b = pts(td_list[3])
		odd_c = pts(td_list[4])
		prob_a = pts(td_list[5])
		prob_b = pts(td_list[6])
		prob_c = pts(td_list[7])
		kelly_a = pts(td_list[8])
		kelly_b = pts(td_list[9])
		kelly_c = pts(td_list[10])
		payout = pts(td_list[11])
		odd_prob_kelly = OddProbKelly(time,update_time,odd_a,odd_b,odd_c,prob_a,prob_b,prob_c,kelly_a,kelly_b,kelly_c,payout)
		print odd_prob_kelly.unicode()
		odd_collection.append(odd_prob_kelly)
	return odd_collection

def process_td_span(td):
	"""
	<td class="bright"><span class="bluetxt">5.50↓</span></td>
	<td>1.40</td>
	"""
	span = td.find('span')
	if span is not None:
		return span.text[:-1]
	return td.text

pts=process_td_span

def parse_main(match_type):
	dt = datetime(2015,5,26)
	match_list = parse_page_jc(dt)

def okooo_main():
	t1 = time.time()
	parse_main(MATCH_TYPE_JC)
	total_time = time.time()-t1
	print "Time used: %f(s)" % total_time
