#!/bin/bash
echo "============================================"
ssh minion1 tail -f /var/log/upstart/kube-proxy.log
echo "============================================"
ssh minion2 tail -f /var/log/upstart/kube-proxy.log
echo "============================================"
ssh minion3 tail -f /var/log/upstart/kube-proxy.log
