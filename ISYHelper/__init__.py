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
        port = config['port']
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
        logging.basicConfig(filename=config['log_file'], format=config['log_format']);
        logger = logging.getLogger('IH')
        # Info by default, unless log_level is debug
        if config['log_level'] == 'debug':
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
    else:
        logger = False
    return logger
