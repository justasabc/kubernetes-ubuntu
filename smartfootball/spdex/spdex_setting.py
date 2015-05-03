from setting import MATCH_TYPE_JC,MATCH_TYPE_M14

SPDEX_CHART_OVERWRITE = True
SPDEX_SAVE_RIGHTNOW = False
# triger now timer to save charts for the first time

url_m14 = "http://c.spdex.com/spdex500a"
url_jc = "http://c.spdex.com/spdex500b"
url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
url_betfair_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
url_betfair_chart_fmt = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId={0}&selectionId={1}&logarithmic={2}"

# global data
GLOBAL_MATCH_PARAMS_SPDEX = {
	MATCH_TYPE_JC  : {"URL":url_jc,"UI_SELECT_ID":"DropJcId","PER_PAGE":8,"ROOT_DIR":"./charts/jc/"},
	MATCH_TYPE_M14 : {"URL":url_m14,"UI_SELECT_ID":"DropLotteryId","PER_PAGE":14,"ROOT_DIR":"./charts/m14/"}
}
GSPDEX = GLOBAL_MATCH_PARAMS_SPDEX

def get_betfair_chart_url(market_id,selection_id,log):
	return url_betfair_chart_fmt.format(market_id,selection_id,log)

def get_betfair_chart_root_dir(match_type,sid):
	# ./charts/jc/    20150501
	# ./charts/m14/    15067
	root_dir = GSPDEX[match_type].get("ROOT_DIR")+sid+"/"
	return root_dir
