* Prerequites
  1. sudo access
  2. user added to docker user group
  # sudo usermod -aG docker $(whoami)

* Build a rally image from Dockerfile
  # cd aurora/docker/buildfiles/centos-rally/ 
  # docker build -t="centos-rally" .
  Alternatively, you can simply pull a docker rally image from Ericsson docker image registry
  # docker pull armdocker.rnd.ericsson.se/proj-de-athlone/openstack-ci/centos-rally
  # docker tag  armdocker.rnd.ericsson.se/proj-de-athlone/openstack-ci/centos-rally:latest centos-rally:latest

* Start a rally container the first time when we don't have a rally db
  Create a dir on host for data persistence
  # sudo mkdir /rally_home
  # sudo chmod 777 /rally_home
  # sudo chcon -Rt svirt_sandbox_file_t /rally_home

  You can clone aurora repo in /rally_homeas there are tests stored in the repo.
  repo name - Project OSS/com.ericsson.de/aurora
  # git clone ssh://ewanliz@gerrit.ericsson.se:29418/OSS/com.ericsson.de/aurora && scp -p -P 29418 ewanliz@gerrit.ericsson.se:hooks/commit-msg aurora/.git/hooks/

  Create a db in a volume in /rally_home on host and mount the volume on the container
  # docker run -t --name rally_container -h rally_container -v /rally_home:/home/rally centos-rally rally db create
  
  Now, we can start an interactive container or run a rally command using a container
  <Inactive Mode> # docker run -it -name rally_container -h rally_container -v /rally_home:/home/rally centos-rally /bin/bash
  # docker run -t --name rally_container -h rally_container -v /rally_home:/home/rally centos-rally rally deployment list

* Start a rally container when we have a rally db already
  # docker run -it --name rally_container -h rally_container -v /rally_home:/home/rally centos-rally /bin/bash

