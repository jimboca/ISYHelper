#!/usr/bin/python
#

from ISYHelper          import load_config,get_logger
#from ISYHelper.Helpers  import Helpers
import ISYHelper.Helpers
from ISYHelper.Helpers.NetScan import NetScan

config = load_config()
foo = object
helper = NetScan(foo,config['helpers'][3])
