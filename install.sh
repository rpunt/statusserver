#!/usr/bin/env bash

sudo apt-get install -y python3-pip python3-dev python3-numpy
sudo pip3 install -r ./requirements.txt

if [ $(sudo raspi-config nonint get_spi) == 0 ]; then
  echo "SPI is enabled"
else
  sudo raspi-config nonint do_spi 0
  echo "SPI is enabled; rebooting"
  sudo reboot
fi

