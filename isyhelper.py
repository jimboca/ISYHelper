#!/usr/bin/python
#
#
# TODO:
# - web.py only allows passing port on command line?!?!?!?
#       - Need to pass current host and port to devices, which is used in foscam1
#

VERSION = "1.10"

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

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor

print('ISYHelper: Version %s Started: %s' % (VERSION, datetime.now()))

# Load the config file.
config = load_config();
print("This host IP is " + config['this_host']['host'])

# Start the log_file
logger = get_logger(config)

# TODO: Move into Devices/init
# Background scheduler for everyone to share.
#executors = {
#    'default': {'type': 'threadpool', 'max_workers': 20},
#    'processpool': ProcessPoolExecutor(max_workers=5)
#}
#job_defaults = {
#    'coalesce': False,
#    'max_instances': 2
#}
#sched = BackgroundScheduler(logger=logger, executors=executors, job_defaults=job_defaults)
sched = BackgroundScheduler(logger=logger)

# Create the helpers now to catch config issues now.
if not 'helpers' in config:
    print("ERROR: helpers not defined in config")
    exit(1)
try:
    helpers = Helpers(logger,sched,config)
except ValueError as e:
    print("ERROR: Configuration " + str(e))
    exit()

if 'ifttt' in config:
    helpers.ifttt = config['ifttt']

# Prepare the REST interface
logger.info("Configuring REST interface...")
rest = REST(config,helpers)
helpers.rest = rest

info = "Starting PyISY: host=" + config['isy']['host'] + " PORT=" + str(config['isy']['port'])
print(info)
logger.info(info)
isy = PyISY.ISY(config['isy']['host'], config['isy']['port'], config['isy']['user'], config['isy']['password'], False, "1.1", logger)
info = " ISY Connected: " + str(isy.connected)
print(info)
logger.info(info)
isy.auto_update = True

# Now that we have the ISY setup, run all the starters
try:
    helpers.start(isy)
except ValueError as e:
    print("ERROR: Helper ISY Setup " + str(e))
    exit()

# Let the scheduler start jobs
sched.start()

# Start the REST interface
# TODO: I'm not really happy with having the rest be an object, since auto-reload does not work
print "Starting REST interface..."
logger.info("Starting REST interface...")
rest.run()
