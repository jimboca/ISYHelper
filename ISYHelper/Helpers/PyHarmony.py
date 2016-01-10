"""

PyHarmony: ISYHelper pyharmony interface

"""

import sys, re
from functools import partial
from .Helper import Helper
sys.path.insert(0,"../pyharmony")

from pyharmony import util as harmony_util

class PyHarmony(Helper):

    def __init__(self,parent,hconfig):
        self.optional = {
                'email'      : { 'default' : None},
                'password'   : { 'default' : None},
                'host'       : { 'default' : None},
                'port'       : { 'default' : '5222'},
        }
        self.pdevices  = []
        super(PyHarmony, self).__init__(parent,hconfig)
        self.lpfx = 'PyHarmony:%s:' % (self.name)
        
    # Schedule the emulator to start immediatly
    def sched(self):
        super(PyHarmony, self).sched()
        
    # Initialize all on startup
    def start(self):
        super(PyHarmony, self).start()
        errors = 0
        self.current_activity_isy = False
        # Setup the Harmony client
        self.parent.logger.info(self.lpfx + " Initializing Client")
        self.client = harmony_util.get_client(self.email, self.password, self.host, self.port)
        self.parent.logger.info(self.lpfx + " Client: " + str(self.client))
        # Print the Harmony Activities to the log
        self.harmony_config = self.client.get_config()
        for a in self.harmony_config['activity']:
            print("%s Activity: %s  Id: %s" % (self.lpfx, a['label'], a['id']))
            self.parent.logger.info(self.lpfx + "Activity: %s  Id: %s" % (a['label'], a['id']))
        
        # Intialize our isy variables
        if self.set_current_activity():
            # Subscribe to changes of the isy variable
            self.handler = self.current_activity_isy.val.subscribe(
                    'changed', partial(self.current_activity_changed))
            self.parent.sched.add_job(self.set_current_activity, 'cron', second='15,45')
        else:
            errors += 1
        if errors > 0:
            raise ValueError("See Log")

    def set_current_activity(self):
        self.current_activity_id  = str(self.client.get_current_activity())
        if not self.current_activity_isy:
            self.current_activity_isy = self.setvar('CurrentActivity',self.current_activity_id);
            if self.current_activity_isy is None:
                return False
        else:
            if self.current_activity_id == str(self.current_activity_isy.val):
                self.parent.logger.debug(self.lpfx + " Already in Activity " + self.current_activity_id + "=" + str(self.current_activity_isy.val))
            else:
                self.parent.logger.info(self.lpfx + " Updating ISY Activity " + self.current_activity_id)
                self.current_activity_isy.val = self.current_activity_id;
        return True

    # This is called when the ISY Variable CurrentActivity is changed, so pass that to the Harmony
    def current_activity_changed(self,e):
        # TODO: Print the activity name info
        cur_id = str(self.client.get_current_activity())
        if cur_id == str(self.current_activity_isy.val):
            self.parent.logger.info(self.lpfx + " Already in Activity " + cur_id + "=" + str(self.current_activity_isy.val))
        else:
            self.parent.logger.info(self.lpfx + " Starting Activity " + str(self.current_activity_isy.val))
            ret = self.client.start_activity(self.current_activity_isy.val)
            self.current_activity_id = int(self.current_activity_isy.val)
            self.parent.logger.info(self.lpfx + " Start=" + str(ret))
