"""
PyISYLink Devices
"""

from .test import Test
from .foscam1 import Foscam1

class Devices(object):

    def __init__(self,logger,devices):
        self.logger = logger
        self.children = []
        self.isy = None
        self.sched = None
        # TODO: I don't like all this dict's, does Python have grep?
        self.by_ip = {}
        self.by_name = {}
        errors = []
        for device in devices:
            # dict by ip for lookup
            try:
                self.add_device(device)
            except ValueError as e:
                errors.append(str(e))
        if len(errors) > 0:
            raise ValueError("\n".join(errors))

    def add_device(self,device):
        self.logger.info("add_device: " + str(device))
        if 'type' not in device:
            raise ValueError("device 'type' not defined for " + str(device))
        # TODO: There must be a good way to use a variable for a class name?
        dtype = device['type']
        if dtype == "Test":
            device_obj = Test(self,device)
        elif dtype == "Foscam1":
            device_obj = Foscam1(self,device)
        else:
            raise ValueError("Unknown device type "+ dtype)
            # TODO: Just create default device?
            return

        self.children.append(device_obj)
        if 'name' in device:
            self.by_name[device['name']] = device_obj
        if 'ip' in device:
            self.by_ip[device['ip']] = device_obj

    # TODO: Add args to allow getting by ip, name, type, ...
    def get_device(self,ip):
        if ip in self.by_ip:
            return self.by_ip[ip]
        self.logger.error("Unable to get device by ip '" + ip + "'");
        return
