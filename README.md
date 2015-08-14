# ISYHelper
Program to assist with communication between ISY994 and anything else.

This is a python program to assist with communicating between the [ISY994i Series Controller](https://www.universal-devices.com/residential/isy994i-series) and any other
device you can access.

The main reason I wrote this was to start learning Python, since I've been stuck in the Perl world for the last 25 years because that is what we use at work.  The reason for Python is that will likely be the most popular way to create virtual node servers with the ISY 5.x firmware, so I want to be ready when that firmware is more stable.

# Configuration

The configuration file is in YAML format, and an example is provided which contains all necessary information.

The Helper is responsible for managing the device and setting the variables on the ISY.  
## name
Each helper has a 'name' which is any name you chose, but must be unique.
## type
The type of helper, which are described in the Helpers section below.

The variables defined by the Helpers will all start with "s.IH." (will make this configurable) followed by the device 'name', followed by the variable name.  For example if you defined your DateAndTime Helper name as 'DT', then it will set variables like "s.IH.DT.Minute" on your ISY.  When isyhelper starts up it will check for the variables that it needs to exist, and will quit with an error if they are not.

# Helpers

ISYHelper defines unique Helper modules for the type of device, and has been written in a way to make adding any new helpers as easy as possible.

Currently there are:

## Test
This is really just a test device for development.

## DateAndTime
Controls setting date and time variables on the ISY.  The following ISY variables can be set
  * Second
  * Minute
  * Hour
  * Day
  * Month
  * Year
The config file allows you to choose the level of updates with the interval option which can be second, minute, hour or day depending on how often you want isyHelper to update, which also determine which variables will be updated on the ISY.

## Foscam1

This Helper communicates with a Foscam cameras that use the [IP Camer CGI Interface](http://www.foscam.es/descarga/ipcam_cgi_sdk.pdf), like the Insteon 75790R which are what I tested with.

The Helper initializes the alarm params on the camera to point back to the REST interface of the isyHelper which sets the Motion variable for the camera when the alarm is triggered, then starts a monitor which checks every 5 seconds if the motion alarm is still enabled or not.  

This will set the ISY variable 'Motion' for the device.

# Install and Run
## Download and configure
Currently there is no installation processes, you must download to try it
- git clone https://github.com/jimboca/ISYHelper
- cd ISYHelper
- cp config.example.yaml config.yaml
- Edit config.yaml for your devices
- ./isyhelper.py

The program will record all information and errors in the log file, to see any errors run 'grep ERROR isyhelper.log'

## Run on startup
- sudo nano /etc/rc.local
- Add this line before the 'exit 0' at the end, where /home/pi is the location you downloaded to.
( cd /home/pi/ISYHelper ; ./isyhelper.py & )

# TODO:
* Generate a list of python modules that need to be installed to use this.  I think this is what is required?
```
sudo pip install datetime
sudo pip install collections
sudo apt-get install libyaml-cpp0.3
sudo pip install pyaml
sudo pip install apscheduler
sudo pip install PyISY
```

**HUGE** Thanks to Automicus (Ryan Kraus) for his https://github.com/automicus/PyISY library which this references.

- AUTHOR: JimBoCA
- DATE: 8/10/2015
- EMAIL: jimboca@gmail.com
