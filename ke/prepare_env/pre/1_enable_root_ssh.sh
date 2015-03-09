#/bin/sh

apt-get -y install openssh-server
# update config
sed -i 's/^PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
service ssh restart


