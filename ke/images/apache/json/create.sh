#/bin/bash
kubecfg -c apache-replicationController.json create replicationControllers
kubecfg -c apache-service.json create services

