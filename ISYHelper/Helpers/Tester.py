"""
Tester Helper
"""

from .Helper import Helper

class Tester(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['ip']
        super(Tester, self).__init__(parent,hconfig)

    def setvar(self,name,value):
        super(Tester, self).setvar(name,value)
