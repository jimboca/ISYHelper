"""
Generic device
"""

class Device(object):

    def __init__(self,parent):
        self.parent   = parent
        self.name     = device['name']
        self.ip       = device['ip']
        self.port     = device['port']
        self.type     = device['type']
        self.model    = device['model']
        self.user     = device['user']
        self.password = device['password']
        self.monitor_job = False

    def setvar(self,name,value):
        print("Device:setvar: " + self.name + " name=" + name + " value="+ str(value))
        # TODO: Catch error
        var = self.parent.isy.variables[2]['s.Pyl.' + self.name + "." + name]
        var.val = value

    def get_data(self,path,payload):
        url = "http://{}:{}/{}".format(self.ip,self.port,path)
        print("Device: get_data: " + url)
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
            print("Connection to the device timed out")
            return
        print("get_data:sent: " + response.url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 400:
            print("Bad request from device %s: %s", self.name, response.text)
        elif response.status_code == 401:
            # Authentication error
            print(
                "Failed to authenticate, "
                "please check your username and password")
            return
        else:
            print("Invalid response from device: %s", response)
