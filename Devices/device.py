"""
Generic device
"""

import requests
from requests.auth import HTTPDigestAuth,HTTPBasicAuth

class Device(object):

    def __init__(self,parent,device):
        self.parent   = parent
        # For now, force all these to be defined
        missing = []
        for key in ['name', 'ip', 'port', 'type', 'model', 'user', 'password']:
            if 'type' not in device:
                missing.append(key)
        if len(missing) > 0:
            raise ValueError("device key(s)" + ",".join(missing) + " not defined for " + str(device))
        self.name     = device['name']
        self.ip       = device['ip']
        self.port     = device['port']
        self.type     = device['type']
        self.model    = device['model']
        self.user     = device['user']
        self.password = device['password']
        self.monitor_job = False

    def setvar(self,name,value):
        self.parent.logger.info("Device:setvar: " + self.name + " name=" + name + " value="+ str(value))
        isy_vname = 's.Pyl.' + self.name + "." + name
        try:
            var = self.parent.isy.variables[2][isy_vname]
        except KeyError:
            self.parent.logger.error('Device:setvar: No ISY Variable "' + isy_vname + '"')
            return
        var.val = value

    def get_data(self,path,payload):
        url = "http://{}:{}/{}".format(self.ip,self.port,path)
        self.parent.logger.info("Device:get_data:send: " + url)
        auth = HTTPDigestAuth(self.user,self.password)
        #auth = (self.user,self.password)
        try:
            response = requests.get(
                url,
                auth=auth,
                params=payload,
                timeout=10
            )
        except requests.exceptions.Timeout:
            self.parent.logger.error("Connection to the device timed out")
            return
        self.parent.logger.info("Device:get_data:success: " + response.url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 400:
            self.parent.logger.error("Bad request from device %s: %s", self.name, response.text)
        elif response.status_code == 401:
            # Authentication error
            self.parent.logger.error(
                "Failed to authenticate, "
                "please check your username and password")
            return
        else:
            self.parent.logger.error("Invalid response from device: %s", response)
