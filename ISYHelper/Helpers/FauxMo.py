"""
FauxMo 1 Helper
"""

from functools import partial
from .Helper import Helper
import sys
sys.path.insert(0,"../fauxmo")
import fauxmo

class device_isy_onoff(object):
    def __init__(self, parent, node):
        self.parent  = parent
        self.node    = node
        
    def on(self):
        self.parent.parent.logger.info('device_isy_on:  ' + str(self.node));
        return self.node.on()
 
    def off(self):
        self.parent.parent.logger.info('device_isy_off: ' + str(self.node));
        return self.node.off()
 
class device_maker_onoff(object):
    def __init__(self, parent, on_event, off_event):
        self.parent    = parent
        self.on_event  = on_event
        self.off_event = off_event
        
    def on(self):
        self.parent.parent.logger.info('device_maker_on:  ' + self.on_event);
        return self.parent.post_ifttt_maker(self.on_event)
 
    def off(self):
        self.parent.parent.logger.info('device_maker_off: ' + self.off_event);
        return self.parent.post_ifttt_maker(self.off_event)
 
class FauxMo(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['devices']
        self.fauxmos  = []
        self.ip = "ifttt.ifttt.com"
        self.port = 443
        self.path = 'foo'
        self.lpfx = 'fauxmo:'
        super(FauxMo, self).__init__(parent,hconfig)
        
    # Schedule the fauxmo to start immediatly
    def sched(self):
        super(FauxMo, self).sched()
        
    # Initialize all on startup
    def start(self):
        super(FauxMo, self).start()
        errors = 0
        for device in self.devices:
            try:
                self.add_device(device)
            except ValueError as e:
                self.parent.logger.error(str(e))
                errors += 1
        lpfx = self.lpfx + ':auto_add_isy:'
        for child in self.parent.isy.nodes.allLowerNodes:
            if child[0] is 'node':
                mnode = self.parent.isy.nodes[child[2]]
                spoken = mnode.spoken
                if spoken is not None:
                    # TODO: Should this be a comman seperate list of which echo will respond?
                    # TODO: Or should that be part of notes?
                    if spoken == '1':
                        spoken = mnode.name
                    self.parent.logger.info(lpfx + " name=" + mnode.name + ", spoken=" + str(spoken))
                    # Is it a controller of a scene?
                    cgroup = mnode.get_groups(responder=False)
                    if len(cgroup) > 0:
                        mnode = self.parent.isy.nodes[cgroup[0]]
                        self.parent.logger.info(lpfx + " is a scene controller of " + str(cgroup[0]) + '=' + str(mnode) + ' "' + mnode.name + '"')
                    self.fauxmos.append([ spoken, device_isy_onoff(self,mnode)])
        #errors += 1
        if errors > 0:
            raise ValueError("See Log")
        self.parent.sched.add_job(partial(fauxmo.run,True,self.fauxmos,logger=self.parent.logger))
        #fauxmo.run(True,self.fauxmos)

    def add_device(self,config):
        self.parent.logger.info(self.lpfx + ' ' + str(config))
        if not 'name' in config:
            raise ValueError("No name defined for " + str(config))
        if not 'type' in config:
            config['type'] = 'ISY'
        if config['type'] == 'ISY':
            #node = self.parent.isy.nodes['Family Room Table']
            dname = config['name']
            if 'address' in config:
                dname = str(config['address'])
            try:
                node = self.parent.isy.nodes[dname]
            except:
                node = self.get_isy_node_by_basename(dname)
            if node is None:
                raise ValueError("Unknown device name or address '" + dname + "'")
            else:
                self.fauxmos.append([ config['name'], device_isy_onoff(self,node)])
        elif config['type'] == 'Maker':
            #if self.config in 'ifttt':
            #    if not self.config['ifttt'] in 'maker_secret_key':
            #        raise ValueError("Missing maker_secret_key in ifttt from config file")
            #else:
            #    raise ValueError("Missing ifttt with maker_secret_key in config file")

            self.fauxmos.append([ config['name'], device_maker_onoff(self,config['on_event'],config['off_event'])])
                
        else:
            raise ValueError("Unknown FauxMo device type " + config['type'])
