import requests
from account import *

url_14_matches = "http://c.spdex.com/spdex500a"
url_jingcai = "http://c.spdex.com/spdex500b"

"""
url_jingcai = "http://c.spdex.com/spdex500b"
001 27427538
002 27427541

url_viewerqq = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id=27427538"

url_bf_biaopan = "http://www.spdex.com/Match/View/BetFair/118393922_746696_0_0"
url_betfair_biaopan = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118393922&selectionId=746696"

<option value='marketId=118393922&selectionId=746696' selected>Amkar
<option value='marketId=118393922&selectionId=50343'>Dinamo Moscow
<option value='marketId=118393922&selectionId=58805'>The Draw

url_home_log_true = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId=118393922&selectionId=50343&asianLineId=0&logarithmic=true"
url_home_log_false = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId=118393922&selectionId=50343&asianLineId=0&logarithmic=false"

url_bf_daxiaoqiu = "http://www.spdex.com/Match/View/BetFair/118393925_47973_0_0"
url_betfair = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId=118393925&selectionId=47973"

"""

def get_page_count(url):
	r = requests.get(url)
	count = 0
	return count

"""
__EVENTTARGET:AspNetPager1
__EVENTARGUMENT:2
__LASTFOCUS:
__VIEWSTATE: 
DropJcId:20150430
AspNetPager1_input:1
"""
def get_all_tids(url):
	payload = {}
	payload['__EVENTTARGET'] = 'AspNetPager1'
	payload['__EVENTARGUMENT'] = 3
	payload['__LASTFOCUS'] = None
	payload['__VIEWSTATE'] = VIEWSTATE
	payload['DropJcId'] = "20150430"
	payload['AspNetPager1_input'] = 3
	r = requests.post(url,data=payload)
	print r.content

def main():
	get_all_tids(url_jingcai)
	print "OK"

if __name__ == "__main__":
	main()
