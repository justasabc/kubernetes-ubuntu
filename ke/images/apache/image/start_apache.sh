#!/bin/bash
# =================================================================================
# https://coreos.com/docs/launching-containers/building/getting-started-with-docker/
# =================================================================================
#source /etc/apache2/envvars
#service apache2 start

/usr/sbin/apache2ctl -D FOREGROUND 
