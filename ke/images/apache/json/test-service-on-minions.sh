#/bin/bash
#curl -L <service_ip>:<service_port>
ip_port=$(kubecfg list services | grep apache-service | awk '{print $4":"$5;}')
echo "curl -L $ip_port"
