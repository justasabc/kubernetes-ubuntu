#==================================================================
# http://opensimulator.org/wiki/Build_Instructions
#==================================================================

FROM ubuntu:base
MAINTAINER Zunlin Ke <zunlinke@example.com>
# non interactive
ENV DEBIAN_FRONTEND noninteractive

# install mono
#RUN apt-get install -y mono-complete && mono --version 
RUN apt-get -y update
RUN apt-get install -y mono-devel && mono --version 
