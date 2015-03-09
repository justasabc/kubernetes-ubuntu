# result
## list pods/services/replicationControllers on master

Name                                   Image(s)                             Host                Labels              Status
----------                             ----------                           ----------          ----------          ----------
a8cc0734-a626-11e4-ac4d-f80f41fa369f   docker-registry:5000/ubuntu:apache   minion3/            name=apache-pod     Running
a8cc65a3-a626-11e4-ac4d-f80f41fa369f   docker-registry:5000/ubuntu:apache   minion1/            name=apache-pod     Running
a8cba5d3-a626-11e4-ac4d-f80f41fa369f   docker-registry:5000/ubuntu:apache   minion2/            name=apache-pod     Running

Name                Labels                                    Selector            IP                  Port
----------          ----------                                ----------          ----------          ----------
apache-service      name=apache-service                       name=apache-pod     192.168.2.128       880
kubernetes          component=apiserver,provider=kubernetes                       192.168.2.125       443
kubernetes-ro       component=apiserver,provider=kubernetes                       192.168.2.146       80

Name                Image(s)                             Selector            Replicas
----------          ----------                           ----------          ----------
apache-controller   docker-registry:5000/ubuntu:apache   name=apache-pod     3

## list containers on minion

### minion1
#### docker ps
CONTAINER ID        IMAGE                                COMMAND                CREATED             STATUS              PORTS                  NAMES
be5ae05fc372        docker-registry:5000/ubuntu:apache   "/bin/bash /home/sta   14 minutes ago      Up 14 minutes                              k8s_apache.f4a7171_a8cc65a3-a626-11e4-ac4d-f80f41fa369f.default.etcd_a8cc65a3-a626-11e4-ac4d-f80f41fa369f_aa4e3b26   
b8513e37a646        kubernetes/pause:go                  "/pause"               14 minutes ago      Up 14 minutes       0.0.0.0:880->880/tcp   k8s_net.f82fac03_a8cc65a3-a626-11e4-ac4d-f80f41fa369f.default.etcd_a8cc65a3-a626-11e4-ac4d-f80f41fa369f_45433d65     

#### iptables -L
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     tcp  --  anywhere             10.10.68.6           tcp dpt:880
ACCEPT     all  --  anywhere             anywhere             ctstate RELATED,ESTABLISHED
ACCEPT     all  --  anywhere             anywhere            
ACCEPT     all  --  anywhere             anywhere            

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         

#### ifconfig
docker0   Link encap:Ethernet  HWaddr 56:84:7a:fe:97:99  
          inet addr:10.10.68.1  Bcast:0.0.0.0  Mask:255.255.255.0
          inet6 addr: fe80::5484:7aff:fefe:9799/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1472  Metric:1
          RX packets:102 errors:0 dropped:0 overruns:0 frame:0
          TX packets:87 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:17335 (17.3 KB)  TX bytes:8804 (8.8 KB)

eth0      Link encap:Ethernet  HWaddr 00:0c:29:ba:07:57  
          inet addr:192.168.1.201  Bcast:192.168.1.255  Mask:255.255.255.0
          inet6 addr: fe80::20c:29ff:feba:757/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:6198017 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1463689 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:2776077112 (2.7 GB)  TX bytes:116725178 (116.7 MB)

flannel0  Link encap:UNSPEC  HWaddr 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  
          inet addr:10.10.68.0  P-t-P:10.10.68.0  Mask:255.255.0.0
          UP POINTOPOINT RUNNING  MTU:1472  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:500 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:9027 errors:0 dropped:0 overruns:0 frame:0
          TX packets:9027 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:1249079 (1.2 MB)  TX bytes:1249079 (1.2 MB)

veth4d81f96 Link encap:Ethernet  HWaddr 76:2e:77:86:2c:1a  
          inet6 addr: fe80::742e:77ff:fe86:2c1a/64 Scope:Link
          UP BROADCAST RUNNING  MTU:1472  Metric:1
          RX packets:19 errors:0 dropped:0 overruns:0 frame:0
          TX packets:22 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:3341 (3.3 KB)  TX bytes:2687 (2.6 KB)





kubecfg resize apache-controller 4

metadata:
  creationTimestamp: 2015-02-03T15:50:06+08:00
  labels:
    name: apache-controller
  name: apache-controller
  namespace: default
  resourceVersion: "295"
  selfLink: /api/v1beta1/replicationControllers/apache-controller?namespace=default
  uid: 44dbc4f7-ab79-11e4-ac4d-f80f41fa369f
spec:
  replicas: 4
  selector:
    name: apache-pod
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: apache-pod
    spec:
      containers:
      - cpu: 200
        image: docker-registry:5000/ubuntu:apache
        imagePullPolicy: ""
        name: apache
        ports:
        - containerPort: 880
          hostPort: 880
          protocol: TCP
      dnsPolicy: ClusterFirst
      restartPolicy:
        always: {}
      volumes: null
status:
  replicas: 2
