#/bin/bash
# apache
kubecfg -c apache-controller.json create replicationControllers
kubecfg -c apache-service.json create services
cd test
./apache.sh
