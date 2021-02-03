#!/bin/bash

set -e

# Set locale to US
echo en_US.UTF-8 UTF-8 > /etc/locale.gen
locale-gen
update-locale LANG=en_US.UTF-8

if [ -f ~/.ssh/id_rsa.pub ]
then
  # add the local ssh key if it exists
  mkdir /home/pi/.ssh/
  cat ~/.ssh/id_rsa.pub | tee -a /home/pi/.ssh/authorized_keys
fi

# enable ssh right away to debug on target
systemctl enable ssh

# install setup dependencies
sudo apt install --yes gpiod python3-pip

# install the application and service
python3 -m pip install -r /opt/qualitair/requirements.txt

# enable the service
systemctl enable qualitair

# configure timezone and hostname
sed -e s/raspberrypi/qualitair/ -i /etc/host{s,name}
ln -snf /usr/share/zoneinfo/Europe/Zurich /etc/localtime

# enable the i2c interface
sudo raspi-config nonint do_i2c 0
echo "dtparam=i2c1=on" >> /boot/config.txt