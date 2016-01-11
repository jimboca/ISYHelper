#!/usr/bin/python
#

from ISYHelper          import load_config,get_logger
#from ISYHelper.Helpers  import Helpers
import ISYHelper.Helpers
from ISYHelper.Helpers.NetScan import NetScan

config = load_config()
foo = object
helper = NetScan(foo,config['helpers'][3])

        for child in self.parent.isy.nodes.allLowerNodes:
            if child[0] is 'node':
                id = child[2]
                spoken = self.parent.isy.nodes[id].spoken
                if spoken is not None:
                    self.fauxmos.append([ spoken, device_isy_onoff(self.parent.isy.nodes[id])])
