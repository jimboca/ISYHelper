"""
Foscam 1 Helper
"""

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
            'http_url': 'http://192.168.1.76:8080/setvar/Motion/1'
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
        self.setvar('Motion',0);

    def setvar(self,name,value):
        super(Foscam1, self).setvar(name,value)
        if name == "Motion":
            if int(value) == 0:
                self.parent.logger.info("Stopping monitor")
                if self.monitor_job is not False:
                    self.monitor_job.remove()
                    self.monitor_job = False
            else:
                self.parent.logger.info("Starting monitor")
                self.monitor_job = self.parent.sched.add_job(
                    self.monitor, 'interval', seconds=10, args=[name,value],
                    name=self.name+".monitor")

    #alarm_regex = re.compile(r'var\s+(.*)=(.*);')
    def monitor(self,name,value):
        lpfx = self.name + ".monitor: "
        self.parent.logger.info(lpfx + "name=" + name + " value="+ str(value))
        data = self.get_data("get_status.cgi",{})
        for item in data.splitlines():
            varl = item.replace('var ','').strip(';').split('=')
            if varl[0] == 'alarm_status':
                self.parent.logger.info(lpfx + varl[0] + '=' + varl[1])
                if str(varl[1]) == '0':
                    self.setvar(name,0)
