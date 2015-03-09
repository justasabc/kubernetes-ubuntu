FROM ubuntu:base
MAINTAINER Zunlin Ke <zunlinke@example.com>

# non interactive
ENV DEBIAN_FRONTEND noninteractive

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set Standard settings (for later use)
#ENV e_root_user root
#ENV e_root_password rootpass
#ENV e_user adminuser
#ENV e_password adminpass
#ENV e_db opensim_80
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# install mysql
#RUN echo "mysql-server mysql-server/root_password password $e_root_password" | debconf-set-selections && \
#    echo "mysql-server mysql-server/root_password_again password $e_root_password" | debconf-set-selections
#RUN apt-get -y install mysql-server mysql-client
# "root" user with password "rootpass", root user only has access from localhost.
# but if we want to connect to container from host, we can not use 'root'.
# so we need to create a user 'opensimuser' with password 'opensimpass' instead.

# Enable remote access (default is localhost only, we change this
# otherwise our database would not be reachable from outside the container)
#RUN sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf

# Add startup file
ADD ./prepare_mysql.sh /home/prepare_mysql.sh

# Run startup script
RUN bin/sh /home/prepare_mysql.sh

ADD ./my.cnf /etc/mysql/my.cnf

# startup
ADD ./start_mysql.sh /home/start_mysql.sh

# Set the default command to run when starting the container
EXPOSE 3306
#CMD ["/bin/bash", "/home/start_mysql.sh"]
