"""

"""

import logging
import logging.handlers
import time
import sys
import yaml
import socket
import os

# from http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
def get_network_ip(rhost):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((rhost, 0))
    return s.getsockname()[0]

def load_config ():
    config_file = open('config.yaml', 'r')
    config = yaml.load(config_file)
    config_file.close
    # host config param overrides default.
    if 'host' in config and config['host'] is not None:
        # use what the user has defined.
        this_host = config['host']
    else:
        # Only way to get the current host ip is connect to something, so use the ISY.
        this_host = get_network_ip(config['isy']['host'])
    # port config param overrides port
    port = '8080'
    if 'port' in config and config['port'] is not None:
        port = str(config['port'])
    print "isyhelper: host: " + this_host + ":" + port
    config['this_host'] = {
        'host' : this_host,
        # TODO: This is the REST interface, should be configurable?
        'port' : port,
    }
    config['this_host']['url'] = 'http://'+config['this_host']['host']+':'+config['this_host']['port']
    config['log_format']       = '%(asctime)-15s:%(name)s:%(levelname)s: %(message)s'
    return config

def get_logger(config):
    if 'log_file' not in config:
        config['log_file'] = False
        print("PyISYLink: No log_file defined")
    elif config['log_file'] == 'none':
        print("PyISYLink: Not writing log because log_file is none")
        config['log_file'] = False

    if config['log_file'] != False:
        print('isyhelper: Writing to log: ' + config['log_file'] + ' level=' + str(config['log_level']))
        if os.path.exists(config['log_file']):
            os.remove(config['log_file'])
        # Create the logger
        logger = logging.getLogger('IH')
        # Set the log level Warning level by default, unless log_level is debug or info
        if config['log_level'] == 'debug':
            logger.setLevel(logging.DEBUG)
        elif config['log_level'] == 'info':
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)
        # Make a handler that writes to a file, 
        # making a new file at midnight and keeping 30 backups
        handler = logging.handlers.TimedRotatingFileHandler(config['log_file'], when="midnight", backupCount=7)
        # Format each log message like this
        formatter = logging.Formatter(config['log_format'])
        # Attach the formatter to the handler
        handler.setFormatter(formatter)
        # Attach the handler to the logger
        logger.addHandler(handler)
    else:
        logger = False
    return logger
