"""

"""

import logging
import yaml
import socket

# from http://commandline.org.uk/python/how-to-find-out-ip-address-in-python/
def get_network_ip(rhost):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((rhost, 0))
    return s.getsockname()[0]

def load_config ():
    config_file = open('config.yaml', 'r')
    config = yaml.load(config_file)
    config_file.close
    # Only way to get the current host ip is connect to something, so use the ISY.
    config['this_host'] = {
        'host' : get_network_ip(config['isy']['host']),
        # TODO: This is the REST interface, should be configurable?
        'port' : '8080',
    }
    config['this_host']['url'] = 'http://'+config['this_host']['host']+':'+config['this_host']['port']
    return config

def get_logger(config):
    if 'log_file' not in config:
        config['log_file'] = False
        print("PyISYLink: No log_file defined")
    elif config['log_file'] == 'none':
        print("PyISYLink: Not writing log because log_file is none")
        config['log_file'] = False

    if config['log_file'] != False:
        print('pylink: Writing to log: ' + config['log_file'])
        logging.basicConfig(filename=config['log_file']);
        logger = logging.getLogger()
        logger.setLevel(0)
    else:
        logger = False
    return logger
