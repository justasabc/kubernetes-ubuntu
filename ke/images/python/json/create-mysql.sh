#/bin/bash
# mysql
kubecfg -c mysql-controller.json create replicationControllers
kubecfg -c mysql-service.json create services
cd test
./mysql.sh
