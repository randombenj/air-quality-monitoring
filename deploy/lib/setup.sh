#!/bin/bash


set -e

# Set locale to US
echo en_US.UTF-8 UTF-8 > /etc/locale.gen
locale-gen
update-locale LANG=en_US.UTF-8

if [ -f ~/.ssh/id_rsa.pub ]
then
  # add the local ssh key if it exists
  cat ~/.ssh/id_rsa.pub | tee -a /home/pi/.ssh/authorized_keys
fi

# enable ssh
systemctl enable ssh

# configure timezone and hostname
sed -e s/raspberrypi/qualitair/ -i /etc/host{s,name}
ln -snf /usr/share/zoneinfo/Europe/Zurich /etc/localtime

# enable the camera
sudo raspi-config nonint do_i2c 0
