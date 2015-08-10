#!/tools/bin/python
#!/usr/bin/python
#
# sudo dpkg-reconfigure tzdata
# sudo apt-get install libyaml-cpp0.3
# sudo pip-3.2 install datetime
# sudo pip-3.2 install collections
# sudo pip-3.2 install pyaml
# sudo pip-3.2 install apscheduler
# 2:
# sudo easy_install apscheduler
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
import ISYHelper

print('PyISYLink: Started: %s' % datetime.now())

# Load the config file.
config = load_config();

# Start the log_file
logger = get_logger(config)

# Background scheduler for everyone to share.
sched = BackgroundScheduler(logger=logger)


# Create the devices first to catch config issues now.
try:
    devices = Devices(logger,config['devices'])
except ValueError as e:
    print("Configuration Errors:\n" + str(e))
    exit()

# Create the devices first to catch config issues now.
try:
    monitors = Monitors(logger,sched,config['monitors'])
except ValueError as e:
    print("Configuration Errors:\n" + str(e))
    exit()

isy = PyISY.ISY(config['isy_host'], config['isy_port'], config['isy_user'], config['isy_password'], False, "1.1", logger)
logger.info("Connected: " + str(isy.connected))
isy.auto_update = True
# TODO: I don't like setting this as attributes, should be functions?
devices.isy = isy
devices.sched = sched
monitors.sched = sched
monitors.isy = isy

# Let the scheduler start jobs
sched.start()

# Start the REST interface
# TODO: I'm not really happy with having the rest be an object, since re-load does not work
logger.info("Starting REST interface...")
rest = isyhelperREST(devices)
devices.rest = rest
rest.run()
