#!/usr/bin/python
#
#
# TODO:
# - Check config params are defined
# - Add config to update every second
# - web.py only allows passing port on command line?!?!?!?
#       - Need to pass current host and port to devices, which is used in foscam1
#

# When run in directory containing downloaded PyIsy
import sys
sys.path.insert(0,"../PyISY")
sys.path.insert(0,"../VarEvents")

# Load our dependancies
from datetime import datetime
import PyISY
import ISYHelper
from ISYHelper          import load_config,get_logger
from ISYHelper.Helpers  import Helpers
from ISYHelper.REST     import REST

#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

print('PyISYLink: Started: %s' % datetime.now())

# Load the config file.
config = load_config();

# Start the log_file
logger = get_logger(config)

# TODO: Move into Devices/init
# Background scheduler for everyone to share.
sched = BackgroundScheduler(logger=logger)

# Create the helpers now to catch config issues now.
if not 'helpers' in config:
    print("ERROR: helpers not defined in config")
    exit(1)
try:
    helpers = Helpers(logger,sched,config['helpers'])
except ValueError as e:
    print("Configuration Errors:\n" + str(e))
    exit()

isy = PyISY.ISY(config['isy_host'], config['isy_port'], config['isy_user'], config['isy_password'], False, "1.1", logger)
logger.info("Connected: " + str(isy.connected))
isy.auto_update = True
# TODO: I don't like setting as attributes, should be functions?
helpers.isy = isy

# Let the scheduler start jobs
sched.start()

# Start the REST interface
# TODO: I'm not really happy with having the rest be an object, since auto-reload does not work
logger.info("Starting REST interface...")
rest = REST(devices)
helpers.rest = rest
rest.run()
