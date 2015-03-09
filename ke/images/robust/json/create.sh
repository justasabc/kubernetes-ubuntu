#/bin/bash
kubecfg -c robust-replicationController.json create replicationControllers
kubecfg -c robust-service.json create services

