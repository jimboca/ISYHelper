"""
Generic monitor
"""

# TODO: start should not be called at init?

class Monitor(object):

    def __init__(self,parent,monitor):
        self.parent   = parent
        # For now, force all these to be defined
        missing = []
        for key in ['name', 'type']:
            if 'type' not in monitor:
                missing.append(key)
        if len(missing) > 0:
            raise ValueError("monitor key(s)" + ",".join(missing) + " not defined for " + str(monitor))
        self.name     = monitor['name']
        self.type     = monitor['type']
        self.start()

    def start(self):
        self.parent.logger.error("No start defined for monitor object " + self.name)
