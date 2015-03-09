#!/bin/bash
echo "====================================================="
e_root_user=root
e_root_password=rootpass
e_user=adminuser
e_password=adminpass
e_db=opensim_80
echo $e_root_user
echo $e_root_password
echo $e_user
echo $e_password
echo $e_db
echo "====================================================="

echo "mysql-server mysql-server/root_password password $e_root_password" | debconf-set-selections && \
echo "mysql-server mysql-server/root_password_again password $e_root_password" | debconf-set-selections
apt-get -y install mysql-server mysql-client

# "root" user with password "rootpass", root user only has access from localhost.
# but if we want to connect to container from host, we can not use 'root'.
# so we need to create a user 'opensimuser' with password 'opensimpass' instead.

# Enable remote access (default is localhost only, we change this
# otherwise our database would not be reachable from outside the container)
sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf

service mysql start
sleep 5s
echo "1====================================================="
service mysql status
echo "2====================================================="

echo "3====================================================="
# create user and grant privileges for opensimuser
mysql -u $e_root_user -p$e_root_password <<EOF
CREATE DATABASE $e_db;
GRANT ALL ON *.* TO '$e_user'@'%' IDENTIFIED BY '$e_password' WITH GRANT OPTION; 
GRANT ALL ON *.* TO '$e_user'@'localhost' IDENTIFIED BY '$e_password' WITH GRANT OPTION; 
GRANT ALL ON *.* TO '$e_user'@'127.0.0.1' IDENTIFIED BY '$e_password' WITH GRANT OPTION; 
FLUSH PRIVILEGES; 
EOF

echo "select users from mysql by admin..."
mysql -u $e_user -p$e_password <<EOF
use mysql;
select User,Host,Password from user;
EOF
echo "4====================================================="
#sleep 2s

echo "5====================================================="
service mysql stop
sleep 3s
service mysql status
echo "6====================================================="
