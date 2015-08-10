"""
PyISYLink DateAndTime Monitor
"""

from .dateandtime import DateAndTime

class Monitors(object):

    def __init__(self,logger,sched,monitors):
        self.logger = logger
        self.children = []
        self.isy = None
        self.sched = sched
        errors = []
        for monitor in monitors:
            try:
                self.add_monitor(monitor)
            except ValueError as e:
                errors.append(str(e))
        if len(errors) > 0:
            raise ValueError("\n".join(errors))

    def add_monitor(self,monitor):
        self.logger.info("add_monitor: " + str(monitor))
        if 'type' not in monitor:
            raise ValueError("monitor 'type' not defined for " + str(monitor))
        # TODO: There must be a good way to use a variable for a class name?
        dtype = monitor['type']
        if dtype == "DateAndTime":
            monitor_obj = DateAndTime(self,monitor)
        else:
            raise ValueError("Unknown monitor type "+ dtype)
            # TODO: Just create default monitor?
            return
        self.children.append(monitor_obj)


    #def get_monitor(self,name):
        #if name in self.by_ip:
        #    return self.by_ip[ip]
        #self.logger.error("Unable to get monitor by ip '" + ip + "'");
        #return
