#!/usr/bin/python
#

import web

# TODO: Move this inside the top object?
# TODO: Allow monitors or devices to add new ones
urls = (
    '/setvar/*(.*)', 'setvar',
    '/(.*)', 'default'
)

# TODO: This is dumb, but I was lazy.  It's a global variable referenced to 
# TODO: find our top object in the lower classes, like setvar.GET.
# TODO: There must be a way to pass this in web.application?
isyhelperRESTObj = False

class PyISYLinkREST(object):

    global isyhelperRESTObj

    def __init__(self,devices):
        global isyhelperRESTObj
        self.app = web.application(urls, globals())
        self.devices = devices
        isyhelperRESTObj = self

    def run(self):
        self.app.run()

class default:

    def GET(self, name):
        if not name:
            name = 'World'
        return 'Default, ' + name + '!'

class setvar:

    def GET(self, path):
        if not path:
            return "varname/value not defined!"
        # TODO: Allow value param to be passed in?
        # TODO: Make sure split only returns 2 objects?
        #udata = web.input(value=None)
        li = path.split("/")
        varname = li[0]
        varvalue = li[1]
        dip = web.ctx['ip']
        # TODO: Generate error if device does not exist
        device = isyhelperRESTObj.devices.get_device(dip)
        info = 'Device: ' + dip + ' varname='+ varname + ' value=' + str(varvalue)
        isyhelperRESTObj.devices.logger.info(info)
        device.setvar(varname,varvalue)
        return info

#if __name__ == "__main__":
#    #PylREST.run()
