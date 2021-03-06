#/usr/bin/python
# -*- coding:utf-8 -*-

# base/apache/var/www/region_load/
# region related
INTERNAL_ADDRESS = "0.0.0.0"
EXTERNAL_HOSTNAME = "162.105.17.48"
ALLOW_ALTERNATE_PORTS = False
MAX_AGENTS = 100
MAX_PRIMS = 15000

GLOBAL_REGION_DATA2 = {
	"huyu": {"orig":(1000,1000), "startPort":9000, "wh":(2,2)},
	"xwd": {"orig":(1005,1000), "startPort":9050, "wh":(2,2)},
	"newhuyu": {"orig":(1010,1000), "startPort":9100, "wh":(2,2)},
	"newxwd": {"orig":(1015,1000), "startPort":9150, "wh":(2,2)},
	"newregion": {"orig":(1020,1000), "startPort":9200, "wh":(2,2)}
	}

CLUSTER_DATA_DIR = "./cluster_data/"

# minions related
MINIONS=["minion1","minion2","minion3"]

# kubernetes related
DOCKER_REGISTRY='docker-registry:5000'
APACHE_NAME='apache'
MYSQL_NAME='mysql'
ROBUST_NAME='robust'

APACHE_IMAGE="docker-registry:5000/ubuntu:apache"
MYSQL_IMAGE="docker-registry:5000/ubuntu:mysql"
ROBUST_IMAGE="docker-registry:5000/ubuntu:robust"

OPENSIM_NAME='opensim'
OPENSIM_IMAGE="docker-registry:5000/ubuntu:opensim"
OPENSIM_COMMAND = ["/bin/bash", "/home/opensim80/bin/ke/start_opensim_xxx.sh"]
CPU = 1024
MEMORY = 1000000000

APACHE_COMMAND = ["/bin/bash", "/home/start_apache.sh"]
MYSQL_COMMAND = ["/bin/bash", "/home/start_mysql.sh"]
ROBUST_COMMAND = ["/bin/bash", "/home/opensim80/bin/ke/start_robust.sh"]

# cpu/memory
