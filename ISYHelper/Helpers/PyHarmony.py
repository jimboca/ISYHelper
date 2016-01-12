"""

PyHarmony: ISYHelper pyharmony interface

"""

import sys, re, json
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
                'spoken_prefix' : { 'default' : None},
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
        self.harmony_config = self.client.get_config()
        #
        # Build a FauxMo Herlper for this device?
        if self.spoken_prefix is not None:
            myfauxmo = {
                'type'       :  "FauxMo",
                'name'       : "FauxMo%s" % (self.name),
                'use_spoken' : False,
                'devices'    : []
            }
            for a in self.harmony_config['activity']:
                # Print the Harmony Activities to the log
                print("%s Activity: %s  Id: %s" % (self.lpfx, a['label'], a['id']))
                self.parent.logger.info(self.lpfx + "Activity: %s  Id: %s" % (a['label'], a['id']))
                myfauxmo['devices'].append(
                    {
                        'name':       "%s %s" % (self.spoken_prefix,a['label']),
                        'type':      'PyHarmony',
                        'type_name': self.name,
                        'command':   'activity',
                        'on_event':  a['id'],
                        'off_event': -1,
                    }
                )
            self.parent.add_helper(myfauxmo)
        
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
            ret = self.start_activity(self.current_activity_isy.val)
            self.current_activity_id = int(self.current_activity_isy.val)
            self.parent.logger.info(self.lpfx + " Start=" + str(ret))

    def start_activity(self,activity):
        ret = self.client.start_activity(activity)
        self.parent.logger.info(self.lpfx + " activity returned:" + str(ret))
        # Always seems to run none?
        if ret is None:
            return True
        return False

    def json_dump(self,obj):
        """Pretty JSON dump of an object."""
        # sort_keys=True, 
        return json.dumps(obj, indent=4, separators=(',', ': '))

    def rest_get(self,web_app,command):
        self.parent.logger.debug("%s rest_get: client=%s command=%s" % (self.lpfx,self.client,str(command)))
        if command[0] == "show":
            if command[1] == "activities":
                return self.json_dump(self.harmony_config['activity'])
            elif command[1] == "devices":
                return self.json_dump(self.harmony_config['device'])
            elif command[1] == "config":
                return self.json_dump(self.harmony_config)
            elif command[1] == "info":
                l = [
                    "Client: %s" % (self.client),
                    "Current Activity: %s" % str(self.client.get_current_activity())
                ]
                for a in self.harmony_config['activity']:
                    # Print the Harmony Activities to the log
                    l.append("Activity: '%s'  Id: %s" % (a['label'], a['id']))
                return "\n".join(l)
            return "unknown show command '%s'" % command[1]

        # TODO: Raise exception?
        return "unknown command '%s'" % command[0]

