# ISYHelper
Program to assist with communication between ISY994 and anything else.

This is a python program to assist with communicating between the [ISY994i Series Controller](https://www.universal-devices.com/residential/isy994i-series) and any other device you can access.

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

## PyHue

This starts a Python Hue Hub Emulator https://github.com/falk0069/hue-upnp that allows the Amazon Echo and Harmony Hub to control and monitor the ISY devices.

To use this, you currently ahve to grab my version from git.  The author is reviewing the changes, and should be merged soon.  In the meantime in the same directory where you have ISYHelper (not inside the ISYHelper directory) run: 
git clone https://github.com/jimboca/hue-upnp as shown in the install instructions below.

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

## FauxMo

This runs the excellent Belkin WeMo emulator https://github.com/makermusings/fauxmo which allows the Amazon Echo to control the ISY and IFTTT Maker!  

To use this, you currently have to grab my version from from git.  So in the same directory where you have ISYHelper (not inside the ISYHelper directory) run:
git clone https://github.com/jimboca/fauxmo as shown in the install instructions below.

See the config.example.yaml for some examples.

### devices
  All information for PyHue devices applies to FauxMo devices, along with the following extras.
  
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

  For the above URL, you can use https if you have a certificate, and your_host_or_ip is for your router name or IP to the outside, and port_num is the port number you set to forward to 8080.  The token must match the token in your config file.

  For the Body:
  - type
  The type of object on the ISY we will set, only variable right now
  - name
  The Variable name to set, varname in the example.  Currently only State variables are supported, not Integers!
  - value
  The Value to set the variable

## Foscam1

This Helper communicates with a Foscam cameras that use the [IP Camer CGI Interface](http://www.foscam.es/descarga/ipcam_cgi_sdk.pdf), like the Insteon 75790R which are what I tested with.

The Helper initializes the alarm params on the camera to point back to the REST interface of the isyHelper which sets the Motion variable for the camera when the alarm is triggered, then starts a monitor which checks every 5 seconds if the motion alarm is still enabled or not.  

This will set the ISY variable 'Motion' for the device.

# Install and Run

## Setup your ISY

If you plan to use the Spoken property from the ISY for FauxMo or PyHue helpers, then you must set them in the ISY before starting isyhelper.  Go to your ISY admin console and Right click on the device or scene you want to control and select 'Notes' then in set 'Spoken' to 1. By setting it to 1 it will use the device name as the spoke name, if you want this to be different then just enter the spoken name you want to use.

## Download and configure

Currently there is no installation processes, you must download to try it.  Also, the python modules listed in the "To Do" section must be installed.

- Install Python libraries we need
  - sudo apt-get install python-pip
  - sudo pip install datetime
  - sudo apt-get install libyaml-cpp0.3
  - sudo pip install pyaml
  - sudo pip install apscheduler
  - sudo pip install PyISY
  - sudo pip install web.py
  - sudo pip install wsgilog
- Create a directory where you want to store it in the home directory
  - cd
  - mkdir isyhelper
  - cd isyhelper
- Grab all the code
  - git clone https://github.com/jimboca/ISYHelper
  - git clone https://github.com/jimboca/PyISY
  - git clone https://github.com/jimboca/fauxmo
  - git clone https://github.com/jimboca/hue-upnp
  - cd ISYHelper
- Configure the helpers you want to use
  - cp config.example.yaml config.yaml
  - nano config.yaml
- ./isyhelper.py

The program will record all information and errors in the log file, to see any errors run 'grep ERROR isyhelper.log', or whatever you set the log to in your config.yaml.

Depending on how many devices you have it can take a minute or more to finish starting up, so wait until you see all 'Starting helper' lines for the helpers you have enabled.

If you start in a terminal like shown and close the terminal then isyhelper will exit.  If you want it to stay running after closing the terminal, start it with the ih.start script

## Run on startup
- sudo nano /etc/rc.local
- Add this line before the 'exit 0' at the end, where /home/pi is the location you downloaded to.
```
( cd /home/pi/isyhelper/ISYHelper ; ./isyhelper.py & )
```

## Restarting

If you started ISYHelper in the forground, then it  not let you stop the program with a control-c.  You must background it with control-z then 'kill %1'.

If it is running from the rc.local script at startup then it is running as root, so you need to find and kill the processs with
...
ps -ef | grep isyh
...
Note the process id which is the second column for the isyhelper process and run kill on that process id


# To Do

## Document how to run as a service

## Other modules that could be used.
For pyharmony?
```
sudo pip install sleekxmpp
```
Only if you are going to use the NMap helper (which isn't released yet)
For some reason 'sudo pip install libnmap' wont work for me?  So had to do it this way:
```
git clone https://github.com/savon-noir/python-libnmap.git
cd python-libnmap
python setup.py install
sudo pip install collections
sudo apt-get install nmap
sudo pip install libnmap
```
If you plan to use SSL (https) for Maker, and you have a real certificate (not self signed) you need to install these as well:
```
sudo apt-get install libffi-dev
sudo apt-get install python-dev
sudo pip install pyOpenSSL
```
Note: It takes a while to compile pyOpenSSL packages like cryptography...

## Multiple responses for large device count

Currently testing sending seperate responses to a query so only one server can be running to handle > 63 devices, which is the documented hue maximum per hub.  I have currently tested 48 devices and it works as expected.  http://www.developers.meethue.com/documentation/bridge-maximum-settings

## Harmony Hub direct

Look into all the options to control harmony hub directly.  Currently looking at pyharmony.

## TiVo

Look into the TiVo interface options for changing channels directly instead of thru the Harmony.

## Spoken for Variables

Plan to add support for a naming convention of variables to specify their spoken name.

# Isssues

- IFTTT Maker Channel does not allow a self-signed certificate, so I have not been able to test...  I need to get a real certificate...

I created one with this info:
  - http://heapkeeper-heap.github.io/hh/thread_1344.html
  - http://www.8bitavenue.com/2015/05/webpy-ssl-support/

- I have only tested this on a RPi with Python 2.7.  I had issues trying to install the web.py module on my RPi with Python 3.2 so if I figure that out I will test with 3.2.

# Known Bugs
* hue-upnp does not die if http_port is in use and can't be started, just issues the message and continues
* ISYHelper is trapping and ignoring control-C, I think this is happening in web.py so need to investagate
* log rolling doesn't seem to be working properly.
  * Deleting old logs does not clear space, have to restart.
  * Seems to be keeping all logs instead of just 7 days worth.

# Versions

* 01/03/2016:  Version: 1.08  Update to latest hue-upnp so IP and PORT can now be passed in.
* 11/21/2015:  Version: 1.07  Fixed for scenes that do not have a controller
* 11/18/2015:  Version: 1.06  Add support for spoken property on scenes.
* 11/15/2015:  Version: 1.05  First official release with PyHue support.  
* 09/07/2015:  Fixed when notes exists, but spoken was empty.  Update to PyISY and ISYHelper
* 09/05/2015:  A new version is released with better automatic support of the Spoken parameter for Amazon Echo.

**HUGE** Thanks to Automicus (Ryan Kraus) for his https://github.com/automicus/PyISY library which this references.

- AUTHOR: JimBoCA
- DATE: 8/10/2015
- EMAIL: jimboca3@gmail.com
