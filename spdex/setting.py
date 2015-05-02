# -*- coding:utf-8 -*-

url_m14 = "http://c.spdex.com/spdex500a"
url_jc = "http://c.spdex.com/spdex500b"
url_viewerqq_fmt = "http://c.spdex.com/iframe/IframeViewerQQ.aspx?id={0}"
url_betfair_fmt = "http://84.20.200.11/betting/LoadRunnerInfoAction.do?marketId={0}&selectionId={1}"
url_betfair_chart_fmt = "http://84.20.200.11/betting/LoadRunnerInfoChartAction.do?marketId={0}&selectionId={1}&logarithmic={2}"

# myfile
IMAGE_CHUNK_SIZE = 256
ROOT_DIR = "./charts/"

SAVE_CHARTS = True
IMAGE_OVERWRITE = True
# if true, program will download images and overwrite local images

# global data
MATCH_TYPE_JC='JC'
MATCH_TYPE_M14="M14"
GLOBAL_MATCH_PARAMS = {
	MATCH_TYPE_JC  : {"URL":url_jc,"UI_SELECT_ID":"DropJcId","PER_PAGE":8,"ROOT_DIR":"./charts/jc/"},
	MATCH_TYPE_M14 : {"URL":url_m14,"UI_SELECT_ID":"DropLotteryId","PER_PAGE":14,"ROOT_DIR":"./charts/m14/"}
}
GDATA = GLOBAL_MATCH_PARAMS
