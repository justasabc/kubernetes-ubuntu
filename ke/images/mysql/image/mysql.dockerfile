#==================================================================
# http://txt.fliglio.com/2013/11/creating-a-mysql-docker-container/
# https://github.com/nkratzke/EasyMySQL/blob/master/Dockerfile
# https://github.com/gegere/coreos-etcd-docker-fleet/blob/develop/Docker/MySQL/Dockerfile
# https://github.com/tutumcloud/tutum-docker-mysql
# http://stackoverflow.com/questions/25135897/how-to-automatically-start-a-service-when-running-a-docker-container
#==================================================================

FROM ubuntu:base
MAINTAINER Zunlin Ke <zunlinke@example.com>

# non interactive
ENV DEBIAN_FRONTEND noninteractive

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set Standard settings (for later use)
ENV e_root_user root
ENV e_root_password rootpass
ENV e_user adminuser
ENV e_password adminpass
ENV e_db opensim_80
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# install mysql
RUN echo "mysql-server mysql-server/root_password password $e_root_password" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password $e_root_password" | debconf-set-selections
RUN apt-get -y install mysql-server mysql-client
# "root" user with password "rootpass", root user only has access from localhost.
# but if we want to connect to container from host, we can not use 'root'.
# so we need to create a user 'opensimuser' with password 'opensimpass' instead.

# Enable remote access (default is localhost only, we change this
# otherwise our database would not be reachable from outside the container)
RUN sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf

# Add startup file
ADD ./prepare_mysql.sh /home/prepare_mysql.sh
# Run startup script
RUN bin/sh /home/prepare_mysql.sh

ADD ./start_mysql.sh /home/start_mysql.sh
#WORKDIR /home

# Note that EXPOSE only works for inter-container links. It doesn't make ports accessible from the host. To expose port(s) to the host, at runtime, use the -p flag.
#EXPOSE 3306

#***********************************************************************************************************
# You need to specify the command to run when container started using CMD or ENTRYPOINT command like below
# Docker container needs the process (last command) keep running, otherwise the container will exit. 
# Therefore normal service mysql start command can't be used directly in Dockerfile

# Solution: In order to keep the process running:
# There are three ways for your Dockerfile normally

# (1) Using service command and append non-end command after that like tail -F
# CMD service mysql start && tail -F /var/log/mysql/error.log

# (2) or use foreground command to do this
# CMD /usr/bin/mysqld_safe

# (3) or wrap your scripts into start.sh and put this in end
# CMD /start.sh
#***********************************************************************************************************

# Set the default command to run when starting the container
#CMD ["bin/sh","/usr/bin/mysqld_safe"]
EXPOSE 3306
#CMD ["/bin/bash", "/home/start_mysql.sh"]
