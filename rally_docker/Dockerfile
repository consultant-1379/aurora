FROM ubuntu:20.04

USER root
RUN export DEBIAN_FRONTEND=noninteractive && \
apt-get update && apt-get install tzdata -qy && \
ln -fs /usr/share/zoneinfo/Europe/Dublin /etc/localtime && \
dpkg-reconfigure --frontend noninteractive tzdata && \
echo "Europe/Dublin" > /etc/timezone && \
#Make sure the package repository is up to date
apt-get -qy full-upgrade && \
apt-get install -qy git && \
# Install a basic SSH server for Jenkins docker plugin
apt-get install -qy openssh-server && \
sed -i 's|session    required     pam_loginuid.so|session    optional     pam_loginuid.so|g' /etc/pam.d/sshd && \
mkdir -p /var/run/sshd && \
# Install JDK 11 for Jenkins docker plugin
apt-get install -qy openjdk-11-jdk && \
# Install other tools
apt-get install -qy  python3-pip wget curl unzip tar gzip sshpass redis-server vim rsync libffi-dev libssl-dev && \
# Add user jenkins to the image
adduser --quiet lciadm100 && \
# Set password for the jenkins user
echo "lciadm100:ericsson123" | chpasswd




# Copy files to set up ssh for gerrit
RUN mkdir /home/lciadm100/.ssh
COPY config /home/lciadm100/.ssh/config
COPY id_rsa /home/lciadm100/.ssh/id_rsa
COPY id_rsa.pub /home/lciadm100/.ssh/id_rsa.pub
 
RUN chown lciadm100:lciadm100 /home/lciadm100/.ssh/id_rsa.pub /home/lciadm100/.ssh/id_rsa /home/lciadm100/.ssh/config /home/lciadm100/.ssh && \
chmod 644 /home/lciadm100/.ssh/id_rsa.pub && \
chmod 600 /home/lciadm100/.ssh/id_rsa && \
chmod 700 /home/lciadm100/.ssh

RUN sed -i s/^deb-src.*// /etc/apt/sources.list

RUN apt-get update && apt-get install --yes sudo python3-dev python3-pip vim git-core && \
    apt clean && \
    pip3 --no-cache-dir install --upgrade pip setuptools && \
    useradd -u 65500 -m rally && \
    usermod -aG sudo rally && \
    echo "rally ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/00-rally-user && \
    mkdir /rally && chown -R rally:rally /rally


RUN pip3 install rally-openstack
RUN pip3 install decorator==4.4.2
RUN pip3 install redis
USER root
RUN /usr/bin/ssh-keygen -A
COPY entrypoint_bash_script.sh entrypoint_bash_script.sh
RUN chmod +x entrypoint_bash_script.sh
EXPOSE 22
EXPOSE 6379
CMD ["./entrypoint_bash_script.sh"]
#CMD ["/usr/sbin/sshd", "-D"]















