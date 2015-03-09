FROM ubuntu:14.04
MAINTAINER Zunlin Ke <zunlinke@example.com>
# non interactive
ENV DEBIAN_FRONTEND noninteractive

# update sources.list
ADD ./sources.list /etc/apt/sources.list

#RUN  rm /etc/apt/sources.list.d/proposed.list 
#ADD ./environment /etc/environment
#ADD ./00proxy /etc/apt/apt.conf.d/00proxy

# update and upgrade
RUN apt-get -y update

# install vim zip
RUN apt-get -y install vim zip 
