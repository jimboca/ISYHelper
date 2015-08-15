"""
Foscam 1 Helper
"""

from functools import partial
from time import sleep
from .Helper import Helper

class Foscam1(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['ip','port','model','user','password']
        self.optional = {
            'set_alarm_params' : { 'default' : {} }
        }
        super(Foscam1, self).__init__(parent,hconfig)
        # Intialize the camera now to make sure we can talk to it.
        # http://www.foscam.es/descarga/ipcam_cgi_sdk.pdf
        force_params = {
            'motion_armed' : '1',
            'http': '1',
            'http_url': self.parent.resturl+'/setvar/Motion/1'
        }
        for key in force_params:
            self.set_alarm_params[key] = force_params[key]
        self.get_data("set_alarm.cgi",self.set_alarm_params)
        self.monitor_job = False

    # Initialize all on startup
    def start(self):
        # Our hash of variables
        self.isy_variables = ['Motion']
        super(Foscam1, self).start()
        # Intialize Motion off
        var = self.setvar('Motion',0);
        # Subscribe to changes
        handler = var.val.subscribe('changed', partial(self.motion_changed,isyvar=var))

    #def setvar(self,name,value):
        #retun super(Foscam1, self).setvar(name,value)

    #alarm_regex = re.compile(r'var\s+(.*)=(.*);')
    def motion_changed(self,e,isyvar):
        lpfx = self.name + ".monitor: "
        self.parent.logger.info(lpfx + " started")
        while isyvar.val != 0:
            sleep(5)
            data = self.get_data("get_status.cgi",{})
            for item in data.splitlines():
                varl = item.replace('var ','').strip(';').split('=')
                if varl[0] == 'alarm_status':
                    self.parent.logger.info(lpfx + varl[0] + '=' + varl[1])
                    if str(varl[1]) == '0':
                        isyvar.val = 0;
