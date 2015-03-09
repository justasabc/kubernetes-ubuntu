#!/bin/bash

# Copyright 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# attempt to warn user about kube and etcd binaries
PATH=$PATH:/opt/bin:

#=====================================================================================
# https://github.com/xinxian0458/kubernetes-ubuntu/blob/master/ubuntu/minion.sh
#=====================================================================================
OPT_BIN=/opt/bin
! test -d $OPT_BIN && mkdir -p $OPT_BIN
cp bin/kubelet $OPT_BIN
cp bin/kube-proxy $OPT_BIN

# ??? need or not ???
#cp bin/kubecfg $OPT_BIN
#cp bin/kubectl $OPT_BIN
#cp bin/kubernetes $OPT_BIN

cp bin/flanneld $OPT_BIN
#=====================================================================================
#=====================================================================================

if ! $(grep Ubuntu /etc/lsb-release > /dev/null 2>&1)
then
    echo "warning: not detecting a ubuntu system"
fi

if ! $(which kube-proxy > /dev/null) && ! $(which kubelet > /dev/null)
then
    echo "warning: kube binaries are not found in the $PATH"
fi

#=====================================================================================
#=====================================================================================
# copy /etc/init files
cp init_conf/kubelet.conf /etc/init/
cp init_conf/kube-proxy.conf /etc/init/
cp init_conf/flanneld_minion.conf /etc/init/flanneld.conf

# copy /etc/initd/ files
cp initd_scripts/kubelet /etc/init.d/
cp initd_scripts/kube-proxy /etc/init.d/
cp initd_scripts/flanneld /etc/init.d/

# copy default configs
cp default_scripts/kubelet /etc/default/
cp default_scripts/kube-proxy /etc/default/
cp default_scripts/flanneld /etc/default/
#=====================================================================================
#=====================================================================================
