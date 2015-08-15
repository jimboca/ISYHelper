
import sys, logging
from wsgilog import WsgiLog
#import config

class WebLog(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = '%(message)s',
            tofile = True,
            toprint = False,
            file = "web.log", #config.log_file,
            interval = 'W0', # config.log_interval,
            backups = 7, #config.log_backups
            )
