FROM centos:7

# install rally dependencies
RUN yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum install -y python-pip  wget git vim sudo gcc python-devel 

# create a new user
RUN useradd rally && \
    usermod -aG wheel rally && \
    echo "rally ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/00-rally-user 


# FIX for ipaddress dependency conflicts issue, pip has its own ipaddress module in _vender dir
RUN mkdir /tmp/python-ipaddress-bkup/ && \
    mv /usr/lib/python2.7/site-packages/ipaddress* /tmp/python-ipaddress-bkup/ 

# install rally
RUN curl https://raw.githubusercontent.com/openstack/rally/master/install_rally.sh | bash
RUN pip install rally-openstack python-openstackclient
RUN rm -rf /root/.cache/

# Use db in mounted volumn
RUN sed -i "s|var/lib/rally/database/rally.sqlite|home/rally/data/rally.db|g" /etc/rally/rally.conf
USER rally
ENV HOME /home/rally
RUN  mkdir -p /home/rally/data
WORKDIR /home/rally

# Docker volumes have specific behavior that allows this construction to work.
# Data generated during the image creation is copied to volume only when it's
# attached for the first time (volume initialization)
#VOLUME ["/home/rally/data"]
#ENTRYPOINT ["rally"]
