# -*- coding:utf-8 -*-
#from termcolor import colored
from datetime import datetime,timedelta
from threading import Timer

from setting import *
from okooo.okooo_setting import *

class OkoooMatchInfo:
	"""
	20150501,001,aaa,bbb,2015/5/1 17:30,27431148
	"""
	def __init__(self,match_id,league,home_name,away_name,match_time,pid,match_status,odd_collection,match_result_obj):
		self.match_id = match_id
		self.league = league
		self.home_name = home_name
		self.away_name = away_name
		self.match_time = match_time
		self.pid = pid
		self.match_status = match_status
		# obj
		self.odd_collection = odd_collection
		self.match_result_obj = match_result_obj

		# set timer
		self.set_timer()

	def unicode(self):
		home_full_score = self.match_result_obj.home_full_score
		away_full_score = self.match_result_obj.away_full_score
		home_half_score = self.match_result_obj.home_half_score
		away_half_score = self.match_result_obj.away_half_score
		return u"{0},{1},{2} VS {3},{4},{5},{6},{7}-{8}".format(self.match_id,self.league,self.home_name,self.away_name,self.match_time,self.pid,self.match_status,home_full_score,away_full_score)

	def set_timer(self):
		p_str = self.unicode()
		print p_str

class MatchResult:

	def __init__(self,match_id,home_full_score,away_full_score,home_half_score,away_half_score):
		self.match_id = match_id
		self.home_full_score = home_full_score
		self.away_full_score = away_full_score
		self.home_half_score = home_half_score
		self.away_half_score = away_half_score

class OddProbKelly:
	def __init__(self,time,update_time,odd_a,odd_b,odd_c,prob_a,prob_b,prob_c,kelly_a,kelly_b,kelly_c,payout):
		self.time = time
		self.update_time = update_time
		self.odd_a = odd_a
		self.odd_b = odd_b
		self.odd_c = odd_c
		self.prob_a = prob_a
		self.prob_b = prob_b
		self.prob_c = prob_c
		self.kelly_a = kelly_a
		self.kelly_b = kelly_b
		self.kelly_c = kelly_c
		self.payout = payout

	def unicode(self):
		#return u"{0},{1},({2},{3},{4}),({5},{6},{7}),({8},{9},{10}),{11}".format(self.time,self.update_time,self.odd_a,self.odd_b,self.odd_c,self.prob_a,self.prob_b,self.prob_c,self.kelly_a,self.kelly_b,self.kelly_c,self.payout)
		return u"{0},({1},{2},{3}),({4},{5},{6}),({7},{8},{9}),{10},{11}".format(self.time,self.odd_a,self.odd_b,self.odd_c,self.prob_a,self.prob_b,self.prob_c,self.kelly_a,self.kelly_b,self.kelly_c,self.payout,self.update_time)

class OddCollection:

	def __init__(self,match_id,okooo_id,bookmaker_id):
		self.match_id = match_id
		self.okooo_id = okooo_id
		self.bookmaker_id = bookmaker_id

		self.odds_list = []

	def append(self,odd):
		self.odds_list.append(odd)
