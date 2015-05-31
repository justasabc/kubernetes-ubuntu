from setting import MATCH_TYPE_JC,MATCH_TYPE_M14

#url_m14_fmt = "http://www.okooo.com/livecenter/zucai/?mf=ToTo&date=15077"
#url_jc_fmt = "http://www.okooo.com/livecenter/jingcai/?date=2015-05-26"
url_jc_fmt = "http://www.okooo.com/livecenter/jingcai/?date={0}"
url_m14_fmt = "http://www.okooo.com/livecenter/zucai/?mf=ToTo&date={0}"
#url_jc_odds_change = "http://www.okooo.com/soccer/match/736957/odds/change/2/"
url_jc_odds_change_fmt = "http://www.okooo.com/soccer/match/{0}/odds/change/{1}/"

def get_url_jc(dt):
	dt_str = dt.strftime("%Y-%m-%d") 
	return url_jc_fmt.format(dt_str)

def get_url_m14(sid):
	return url_jc_m14.format(sid)

def get_url_odds_change(okooo_id,bookmaker_id=2):
	return url_jc_odds_change_fmt.format(okooo_id,bookmaker_id)	

OKOOO_BOOKMAKER_DATA = {
	"jingcai":2,
}
