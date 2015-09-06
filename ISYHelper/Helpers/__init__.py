"""
PyISYLink Helpers
"""

from .Tester      import Tester
from .Foscam1     import Foscam1
from .DateAndTime import DateAndTime
from .Maker       import Maker
from .FauxMo      import FauxMo

class Helpers(object):

    def __init__(self,logger,sched,resturl,helper_configs):
        self.logger = logger
        self.resturl = resturl
        self.children = []
        self.isy = None
        self.sched = sched
        # TODO: I don't like all this dict's, does Python have grep?
        self.by_ip = {}
        self.by_name = {}
        errors = 0
        for hconfig in helper_configs:
            try:
                self.add_helper(hconfig)
            except ValueError as e:
                logger.error(str(e))
                errors += 1
        if errors > 0:
            raise ValueError("See Log")

    def add_helper(self,hconfig):
        self.logger.info("add_helper: " + str(hconfig))
        if 'type' not in hconfig:
            self.logger.error("helper 'type' not defined for " + str(hconfig))
            raise ValueError("See Log")
        # TODO: There must be a good way to use a variable for a class name?
        dtype = hconfig['type']
        print("Initializing new helper: " + dtype)
        if dtype == "Tester":
            helper = Tester(self,hconfig)
        elif dtype == "Foscam1":
            helper = Foscam1(self,hconfig)
        elif dtype == "DateAndTime":
            helper = DateAndTime(self,hconfig)
        elif dtype == "Maker":
            helper = Maker(self,hconfig)
        elif dtype == "FauxMo":
            helper = FauxMo(self,hconfig)
        else:
            self.logger.error("Unknown helper type "+ dtype)
            raise ValueError("See Log")
            return
        self.children.append(helper)
        if 'name' in hconfig:
            self.by_name[hconfig['name']] = helper
        if 'ip' in hconfig:
            self.by_ip[hconfig['ip']] = helper
        # Run the scheduler
        print("  Scheduling helper: " + helper.name)
        helper.sched()
        return helper

    def start(self,isy):
        self.isy = isy
        errors = 0
        for helper in self.children:
            try:
                print("Starting helper: " + helper.name)
                helper.start()
            except ValueError:
                errors += 1
        if errors:
            raise ValueError(str(errors) + " startup errors, see log")

    # TODO: Add args to allow getting by ip, name, type, ...
    def get_helper(self,ip):
        if ip in self.by_ip:
            return self.by_ip[ip]
        self.logger.error("Unable to get helper by ip '" + ip + "'");
        return False

    def get_helper_by_name(self,name):
        if name in self.by_name:
            return self.by_name[name]
        self.logger.error("Unable to get helper by name '" + name + "'");
        return
