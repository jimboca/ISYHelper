"""
Nmap Helper
"""

import logging
from .Helper      import Helper

_LOGGER = logging.getLogger(__name__)

class Asuswrt(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['method', 'host' ]
        self.optional = {
            'user'     : { 'default' : None },
            'password' : { 'default' : None }
        }
        super(Asuswrt, self).__init__(parent,hconfig)
        print("NetScan: method="+self.method)

    def setvar(self,name,value):
        super(Asuswrt, self).setvar(name,value)
