#!/bin/bash

#git clone https://github.com/jimboca/ISYHelper
#ISYHelper/install.sh
cd ..
#sudo apt-get install python-pip
sudo pip install datetime
sudo apt-get install libyaml-cpp0.3
sudo pip install pyaml
sudo pip install apscheduler
sudo pip install PyISY
sudo pip install Flask
sudo pip install wsgilog
sudo pip install sleekxmpp
sudo pip install pyharmony
git clone https://github.com/jimboca/PyISY
git clone https://github.com/jimboca/fauxmo
git clone https://github.com/jimboca/hue-upnp
cd ISYHelper

#cp config.example.yaml config.yaml
#nano config.yaml
