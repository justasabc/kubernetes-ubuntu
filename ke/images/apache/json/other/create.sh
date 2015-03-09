#/bin/bash
kubecfg -c apache-pod.json create pods
kubecfg -c apache-replicationController.json create replicationControllers
kubecfg resize apache-controller 4
kubecfg -c apache-service.json create services

