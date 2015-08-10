"""
Foscam 1 devices
"""

from .device import Device

class Test(Device):

    def __init__(self,parent,device):
        super(Test, self).__init__(parent,device)

    def setvar(self,name,value):
        super(Test, self).setvar(name,value)
