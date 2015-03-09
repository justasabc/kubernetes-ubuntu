#/bin/bash
kubecfg -c mysql-replicationController.json create replicationControllers
kubecfg -c mysql-service.json create services

