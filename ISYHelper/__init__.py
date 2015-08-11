"""

"""

import logging
import yaml

def load_config ():
    config_file = open('config.yaml', 'r')
    config = yaml.load(config_file)
    config_file.close
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
        info = "Startinsg PyISY: host=" + config['isy_host'] + " PORT=" + str(config['isy_port'])
        logger.info(info)
    else:
        logger = False
    return logger
