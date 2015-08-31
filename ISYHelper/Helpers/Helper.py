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
            raise ValueError("helper key(s)" + ",".join(missing) +
                " not defined for " + str(hconfig))
        if hasattr(self,'optional'):
            for key in self.optional:
                if key in hconfig:
                    # Is there a valid list?
                    if 'valid' in self.optional[key]:
                        if hconfig[key] in self.optional[key]['valid']:
                            setattr(self,key,hconfig[key])
                        else:
                            raise ValueError("helper option " + key + ":"+
                                hconfig[key] + " not valid, must be one of " +
                                ",".join(self.optional[key]['valid']))
                    else:
                        setattr(self,key,hconfig[key])
                else:
                    setattr(self,key,self.optional[key]['default'])
        self.isyvp    = "s.IH." + self.name + "."
        # TODO: Check for unknown keys? e.g. must be in required or optional

    # Default scheduler for all
    def sched(self):
        pass

    # Default starter for all
    def start(self):
        if not hasattr(self,'isy_variables'):
            self.isy_variables = []
        errors = 0
        for key in self.isy_variables:
            isy_vname = self.isyvp+key
            try:
                setattr(self,key,self.parent.isy.variables[2][isy_vname])
            except KeyError:
                self.parent.logger.error('Helper:start: No ISY Variable "' + isy_vname + '"')
                errors += 1
        if errors:
            raise ValueError("Missing ISY Variables, see log")

    def varname(self,name):
        return self.isyvp + name

    def existvar(self,name):
        isy_vname = self.varname(name)
        try:
            var = self.parent.isy.variables[2][isy_vname]
        except KeyError:
            return None
        return var

    def getvar(self,name):
        var = self.existvar(name)
        if var is None:
            self.parent.logger.error('helper:getvar: No ISY Variable "' + self.varname(name) + '"')
            return None
        return var

    def setvar(self,name,value):
        self.parent.logger.info("helper:setvar: " + self.name + " name=" + name + " value="+ str(value))
        var = self.getvar(name)
        if var is None:
            return var
        var.val = value
        return var

    def post_ifttt_maker(self,event):
        url = 'https://maker.ifttt.com:443/trigger/{}/with/key/{}'.format(event,self.parent.ifttt['maker_secret_key'])
        self.parent.logger.info("helper:post_ifttt_maker:send: " + url)
        try:
            response = requests.post(
                url,
                timeout=10
            )
        except requests.exceptions.Timeout:
            self.parent.logger.error("Connection to the maker.ifttt timed out")
            return False
        self.parent.logger.info("helper:post_ifttt_maker:success: " + response.url)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            self.parent.logger.error("Bad request from helper %s: %s", self.name, response.text)
        elif response.status_code == 401:
            # Authentication error
            self.parent.logger.error(
                "Failed to authenticate, "
                "please check your username and password")
            return
        else:
            self.parent.logger.error("Invalid response from maker.ifttt: %s", response)
        return False
    
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
