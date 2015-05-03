# -*- coding:utf-8 -*-
# myfile
IMAGE_CHUNK_SIZE = 256
ROOT_DIR = "./charts/"
# if true, program will download images and overwrite local images

MATCH_TOTLA_MINUTES = 105+5

# match status
MATCH_STATUS_NOT_STARTED = 1
MATCH_STATUS_RUNNING = 2
MATCH_STATUS_FINISHED = 3
def get_match_status(now,start_time,end_time):
	if now < start_time:
		return MATCH_STATUS_NOT_STARTED
	elif now < end_time:
		return MATCH_STATUS_RUNNING
	else:
		return MATCH_STATUS_FINISHED

# match type
MATCH_TYPE_JC='JC'
MATCH_TYPE_M14="M14"
