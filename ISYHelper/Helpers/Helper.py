"""
Generic helper
"""

import requests
from requests.auth import HTTPDigestAuth,HTTPBasicAuth

class Helper(object):

    def __init__(self,parent,hconfig):
        self.parent   = parent
        if not hasattr(self,'required'):
            self.required = []
        self.required.append('name')
        self.required.append('type')
        #self.required = ['name', 'ip', 'port', 'type', 'model', 'user', 'password']
        # For now, force all these to be defined
        missing = []
        for key in self.required:
            if key in hconfig:
                setattr(self,key,hconfig[key])
            else:
                missing.append(key)
        if len(missing) > 0:
            raise ValueError("helper key(s)" + ",".join(missing) + " not defined for " + str(hconfig))
        if hasattr(self,'optional'):
            for key,value in self.optional:
                if key in hconfig:
                    setattr(self,key,hconfig[key])
                else:
                    setattr(self,key,value)
        # TODO: Check for unknown keys, e.g. must be in required or optional

    # Default scheduler for all
    def sched(self):
        pass

    def setvar(self,name,value):
        self.parent.logger.info("helper:setvar: " + self.name + " name=" + name + " value="+ str(value))
        isy_vname = 's.Pyl.' + self.name + "." + name
        try:
            var = self.parent.isy.variables[2][isy_vname]
        except KeyError:
            self.parent.logger.error('helper:setvar: No ISY Variable "' + isy_vname + '"')
            return
        var.val = value

    def get_data(self,path,payload):
        url = "http://{}:{}/{}".format(self.ip,self.port,path)
        self.parent.logger.info("helper:get_data:send: " + url)
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
            self.parent.logger.error("Connection to the helper timed out")
            return
        self.parent.logger.info("helper:get_data:success: " + response.url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 400:
            self.parent.logger.error("Bad request from helper %s: %s", self.name, response.text)
        elif response.status_code == 401:
            # Authentication error
            self.parent.logger.error(
                "Failed to authenticate, "
                "please check your username and password")
            return
        else:
            self.parent.logger.error("Invalid response from helper: %s", response)
