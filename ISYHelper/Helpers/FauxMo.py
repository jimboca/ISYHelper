"""
FauxMo 1 Helper
"""

from functools import partial
from .Helper import Helper
import sys
sys.path.insert(0,"../fauxmo")
import fauxmo

class device_isy_onoff(object):
    def __init__(self, node):
        self.node = node
        
    def on(self):
        print('Set: ' + str(self.node) + " on");
        return self.node.on()
 
    def off(self):
        print('Set: ' + str(self.node) + " off");
        return self.node.off()
 
class device_maker_onoff(object):
    def __init__(self, parent, on_event, off_event):
        self.parent    = parent
        self.on_event  = on_event
        self.off_event = off_event
        
    def on(self):
        print('Run: ' + self.on_event);
        return self.parent.post_ifttt_maker(self.on_event)
 
    def off(self):
        print('Run: ' + self.off_event);
        return self.parent.post_ifttt_maker(self.off_event)
 
class FauxMo(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['devices']
        self.fauxmos  = []
        self.ip = "ifttt.ifttt.com"
        self.port = 443
        self.path = 'foo'
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
        for child in self.parent.isy.nodes.allLowerNodes:
            if child[0] is 'node':
                id = child[2]
                spoken = self.parent.isy.nodes[id].spoken
                if spoken is not None:
                    # TODO: Should this be a comman seperate list of which echo will respond?
                    # TODO: Or should that be part of notes?
                    if spoken == '1':
                        spoken = self.parent.isy.nodes[id].name
                    print("FauxMo:add_isy_device: " + str(spoken))
                    self.fauxmos.append([ spoken, device_isy_onoff(self.parent.isy.nodes[id])])

        if errors > 0:
            raise ValueError("See Log")
        fauxmo.run(True,self.fauxmos)

    def add_device(self,config):
        print("FauxMo:add_device: " + str(config))
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
                self.fauxmos.append([ config['name'], device_isy_onoff(node)])
        elif config['type'] == 'Maker':
            #if self.config in 'ifttt':
            #    if not self.config['ifttt'] in 'maker_secret_key':
            #        raise ValueError("Missing maker_secret_key in ifttt from config file")
            #else:
            #    raise ValueError("Missing ifttt with maker_secret_key in config file")

            self.fauxmos.append([ config['name'], device_maker_onoff(self,config['on_event'],config['off_event'])])
                
        else:
            raise ValueError("Unknown FauxMo device type " + config['type'])
