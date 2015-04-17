# robust
kubecfg -c robust-controller.json create replicationControllers
kubecfg -c robust-public-service.json create services
kubecfg -c robust-internal-service.json create services
cd test
./robust.sh
