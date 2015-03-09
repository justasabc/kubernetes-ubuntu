#/bin/bash
ip=$(kubecfg list services | grep mysql-service | awk '{print $4;}')
port=$(kubecfg list services | grep mysql-service | awk '{print $5;}')
echo "mysql -u adminuser -padminpass -P $port -h $ip"
