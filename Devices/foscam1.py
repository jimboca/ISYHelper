"""
Foscam 1 devices
"""

from .device import Device

class Foscam1(Device):

    def __init__(self,parent,device):
        super(Foscam1, self).__init__(parent,device)
        # TODO: We should set by calling monitor.  But then we don't have a monitor running...
        #self.setvar('motion',0);
        params = {
            'motion_armed' : '1',
            'http': '1',
            'http_url': 'http://192.168.1.76:8080/setvar/motion/1'
        }
        self.get_data("set_alarm.cgi",params)

    def setvar(self,name,value):
        super(Foscam1, self).setvar(name,value)
        if name == "motion":
            if int(value) == 0:
                self.parent.logger.info("Stopping monitor")
                if self.monitor_job is not False:
                    self.monitor_job.remove()
                    self.monitor_job = False
            else:
                # TODO: Need multiple monitors based on name
                self.parent.logger.info("Starting monitor")
                self.monitor_job = self.parent.sched.add_job(self.monitor, 'interval', seconds=10, args=[name,value])

    #alarm_regex = re.compile(r'var\s+(.*)=(.*);')
    def monitor(self,name,value):
        self.parent.logger.info("Foscam1:monitor: "+ self.name + " name=" + name + " value="+ str(value))
        data = self.get_data("get_status.cgi",{})
        #sprint("PylDevice:monitor: data=" + data)
        for item in data.splitlines():
            varl = item.replace('var ','').strip(';').split('=')
            if varl[0] == 'alarm_status':
                self.parent.logger.info('Foscam1:monitor: ' + varl[0] + '=' + varl[1])
                if str(varl[1]) == '0':
                    self.setvar(name,0)
