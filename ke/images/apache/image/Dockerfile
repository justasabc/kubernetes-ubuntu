FROM docker-registry:5000/ubuntu:base

# install apache
RUN apt-get install -y apache2

# add files
ADD ./conf/ports.conf /etc/apache2/
ADD ./conf/virgeo_resource.conf /etc/apache2/sites-available/
RUN ln -s /etc/apache2/sites-available/virgeo_resource.conf /etc/apache2/sites-enabled/

# Set Apache environment variables (can be changed on docker run with -e)
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_PID_FILE /var/run/apache2.pid
ENV APACHE_RUN_DIR /var/run/apache2
ENV APACHE_LOCK_DIR /var/lock/apache2
ENV APACHE_SERVERADMIN admin@localhost
ENV APACHE_SERVERNAME localhost
ENV APACHE_SERVERALIAS docker.localhost
ENV APACHE_DOCUMENTROOT /var/www

# startup
ADD ./start_apache.sh /home/start_apache.sh

# add mapping-volumes
# ADD /volumes/var/www /var/www

EXPOSE 880
#CMD ["/bin/bash", "/home/start_apache.sh"]
