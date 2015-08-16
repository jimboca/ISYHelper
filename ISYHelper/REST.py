#!/usr/bin/python
#

import web
from .weblog import WebLog
from web.wsgiserver import CherryPyWSGIServer

# TODO: Move this inside the top object?
# TODO: Allow monitors or devices to add new ones
urls = (
    '/setvar/*(.*)', 'setvar',
    '/maker/*(.*)', 'maker',
    '/(.*)', 'default'
)

# TODO: This is dumb, but I was lazy.  It's a global variable referenced to
# TODO: find our top object in the lower classes, like setvar.GET.
# TODO: There must be a way to pass this in web.application?
isyhelperRESTObj = False


class REST(object):

    global isyhelperRESTObj

    def __init__(self,config,helpers):
        global isyhelperRESTObj
        self.app = web.application(urls, globals())
        self.config = config
        self.helpers = helpers
        isyhelperRESTObj = self
        # TODO: Check thatthe files exist!
        if 'ssl' in self.config:
            if 'certificate' in self.config['ssl']:
                print('Using certificate: '  + self.config['ssl']['certificate'])
                CherryPyWSGIServer.ssl_certificate = self.config['ssl']['certificate']
            if 'private_key' in self.config['ssl']:
                print('Using private_key: ' + self.config['ssl']['private_key'])
                CherryPyWSGIServer.ssl_private_key = self.config['ssl']['private_key']

    def run(self):
        web.config.log_file = self.config['log_file']
        self.app.run(WebLog)

class default:

    def GET(self, name):
        raise web.forbidden()

    def POST(self, name):
        raise web.forbidden()

class setvar:

    def GET(self, path):
        # This is the callers IP.
        dip = web.ctx['ip']
        # Get the helper for the incoming IP address
        helper = isyhelperRESTObj.helpers.get_helper(dip)
        if helper is False:
            web.forbidden()
        if not path:
            raise web.notfound("path not defined from "+dip+"!")
        # TODO: Allow value param to be passed in?
        # TODO: Make sure split only returns 2 objects?
        #udata = web.input(value=None)
        li = path.split("/")
        varname = li[0]
        varvalue = li[1]
        info = 'REST:setvar:GET: ' + dip + ' varname='+ varname + ' value=' + str(varvalue)
        isyhelperRESTObj.helpers.logger.info(info)
        helper.setvar(varname,varvalue)
        return info

class maker:
    def GET(self,path):
        # Not allowed yet.
        web.forbidden()

    def POST(self,path):
        # This is the callers IP.
        dip = web.ctx['ip']
        # Get the helper for the incoming IP address
        helper = isyhelperRESTObj.helpers.get_helper_by_name('Maker')
        if helper is False:
            raise web.notfound("No Maker Helper defined")
        helper.maker(path,web.data())



#if __name__ == "__main__":
#    #PylREST.run()
