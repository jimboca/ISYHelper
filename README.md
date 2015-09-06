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

## ssl

You can enable SSL by setting the certificate and private_key params to point to your files.

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

## FauxMo

This runs the excellent Belkin WeMo emulator https://github.com/makermusings/fauxmo which allows the Amazon Echo to control the ISY and IFTTT Maker!  

To use this, you currently have to grab my version from from git.  So in the same directory where you have ISYHelper (not inside the ISYHelper directory) run:
git clone https://github.com/jimboca/fauxmo as shown in the install instructions below.

See the config.example.yaml for some examples.

### devices

By default all devices that have a 'Spoken' property set in the ISY notes will be added to the list.  To set this right click on the device in the ISY admin console and select 'Notes'.  If you have a recent version of the ISY fireware and admin console you should see the option to add 'Spoken'.  If you want the spoken name to always match the device name, just make the value of the Spoken property be the number one '1', without the quotes.

You only need to hard code the device in the config for devices that do not have the Spoken property set. You can find all your device names and address http://your_isy_ip/rest/nodes

To control a scene that has a controller, just set the Spoken property on the controller of the scene in the admin console.  If the scene does not have a controller, you will have to add it to the config file.

IMPORTANT: Currently if you 'group device' it will not find your Spoken property on your devie.  This is an issue with the PyISY library that I will try to fix soon because almost all my devices were grouped.

  * name
    Currently the name must be specified, and can be the full full path to the device name in your folder hierarchy, or just the device name.  This will also be what you call the device for Alexa, unless the spoken param is set below.
  * address
    This is the device or scene address.  This is not required if name is the real device name.
  * spoken
    You can add a device by name, then set spoken to have the spoken name be different than the device name.
  * type
    This can be 'ISY' or 'Maker', and the default is 'ISY' if not specified.
  * on_event
    This is the Maker IFTTT event to turn the device on
  * off_event
    This is the Maker IFTTT event to turn the device off

Note that each time you start isyhelper.py, you must tell Alexa to 'discover devices'.  This is because the port numbers for each device are random so they are likely different each time.

## Maker

Receives IFTTT Maker requests.  This is the intial version of Maker support, so it will likely change based on feedback from everyone.

Currently the 'name' and 'type' must be 'Maker' in your config file.  You must set the 'token' to something, it's like a lame password...

You must forward a port on your router to the IP address of the device runing ISYHelper port 8080.  (Yes it's hardcode to 8080, I need to add a config param...)

### Maker Setup

- Setup your [Maker channel on IFTTT](https://ifttt.com/maker)
- Click on the "Make a web request" on that page
- Set the Trigger to what you want
- Set the Action:
  - URL: http://your_host_or_ip:port_num/maker
  - Method: POST
  - Content Type: application/json
  - Body:  { "token" : "my_secret_token", "type" : "variable", "name" : "varname", "value" : "1" }

  For the above, you can use https if you have a certificate, and your_host_or_ip is for your router name or IP to the outside, and port_num is the port number you set to forward to 8080.  The token must match the token in your config file.

  For the Body:
  - type
  The type of object on the ISY we will set, only variable right now
  - name
  The Variable name to set, varname in the example
  - value
  The Value to set the variable

## Foscam1

This Helper communicates with a Foscam cameras that use the [IP Camer CGI Interface](http://www.foscam.es/descarga/ipcam_cgi_sdk.pdf), like the Insteon 75790R which are what I tested with.

The Helper initializes the alarm params on the camera to point back to the REST interface of the isyHelper which sets the Motion variable for the camera when the alarm is triggered, then starts a monitor which checks every 5 seconds if the motion alarm is still enabled or not.  

This will set the ISY variable 'Motion' for the device.

# Install and Run
## Download and configure
Currently there is no installation processes, you must download to try it.  Also, the python modules listed in the "To Do" section must be installed.

- Create a directory where you want to store it:
  - mkdir isyhelper
  - cd isyhelper
- git clone https://github.com/jimboca/ISYHelper
- git clone https://github.com/jimboca/PyISY
- git clone https://github.com/jimboca/fauxmo
- cd ISYHelper
- cp config.example.yaml config.yaml
- Edit config.yaml for your devices
- ./isyhelper.py

The program will record all information and errors in the log file, to see any errors run 'grep ERROR isyhelper.log', or whatever you set the log to in your config.yaml.

If you start in a terminal like shown and close the terminal then isyhelper will exit.  If you want it to stay running after closing the terminal, start it with:
  - ./isyhelper.py > ihs.log 2>&1 &
This will be fixed in a future version...

## Run on startup
- sudo nano /etc/rc.local
- Add this line before the 'exit 0' at the end, where /home/pi is the location you downloaded to.
```
( cd /home/pi/ISYHelper ; ./isyhelper.py & )
```

# To Do
* Generate a complete list of python modules that need to be installed to use this.  I think this is what is required?
```
sudo pip install datetime
sudo pip install collections
sudo apt-get install libyaml-cpp0.3
sudo pip install pyaml
sudo pip install apscheduler
sudo pip install PyISY
sudo pip install web.py
sudo pip install wsgilog
sudo apt-get install nmap
sudo pip install libnmap
```
Only if you are going to use the NMap helper (which isn't released yet)
For some reason 'sudo pip install libnmap' wont work for me?  So had to do it this way:
```
git clone https://github.com/savon-noir/python-libnmap.git
cd python-libnmap
python setup.py install
```
If you plan to use SSL (https) for Maker, and you have a real certificate (not self signed) you need to install these as well:
```
sudo apt-get install libffi-dev
sudo apt-get install python-dev
sudo pip install pyOpenSSL
```
Note: It takes a while to compile pyOpenSSL packages like cryptography...

# Isssues

- IFTTT Maker Channel does not allow a self-signed certificate, so I have not been able to test...  I need to get a real certificate...

I created one with this info:
  - http://heapkeeper-heap.github.io/hh/thread_1344.html
  - http://www.8bitavenue.com/2015/05/webpy-ssl-support/

- I have only tested this on a RPi with Python 2.7.  I had issues trying to install the web.py module on my RPi with Python 3.2 so if I figure that out I will test with 3.2.



**HUGE** Thanks to Automicus (Ryan Kraus) for his https://github.com/automicus/PyISY library which this references.

- AUTHOR: JimBoCA
- DATE: 8/10/2015
- EMAIL: jimboca3@gmail.com
