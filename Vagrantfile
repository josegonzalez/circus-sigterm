# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/ubuntu-14.04"
  config.vm.provision "shell", inline: <<-SHELL
    export DEBIAN_FRONTEND=noninteractive
    apt-get update > /dev/null
    apt-get install -qq -y --force-yes libreadline-dev libncurses5-dev libpcre3-dev libssl-dev libxml2-dev libxslt1-dev perl git-core > /dev/null
    apt-get install -qq -y --force-yes python python-dev python-pip > /dev/null
    apt-get install -qq -y --force-yes libzmq-dev python-setuptools python-zmq > /dev/null
    sudo pip install -q circus==0.13 > /dev/null
    PYTHONUNBUFFERED=1 circusd --daemon /vagrant/test.ini > /dev/null
    echo "circusd daemon is running"
  SHELL
end
