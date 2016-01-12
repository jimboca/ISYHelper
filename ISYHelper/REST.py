#!/usr/bin/python
#

import sys
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

# From: http://webpy.org/docs/0.3/api#web.httpserver
class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

#if __name__ == "__main__":
#    app = MyApplication(urls, globals())
#    app.run(port=8888)

class REST(object):

    global isyhelperRESTObj

    def __init__(self,config,helpers):
        global isyhelperRESTObj
        #self.app = web.application(urls, globals())
        self.app = MyApplication(urls, globals())
        self.config = config
        self.helpers = helpers
        isyhelperRESTObj = self
        # TODO: Check that the files exist!
        if 'ssl' in self.config:
            if 'certificate' in self.config['ssl']:
                print('Using certificate: '  + self.config['ssl']['certificate'])
                CherryPyWSGIServer.ssl_certificate = self.config['ssl']['certificate']
            if 'private_key' in self.config['ssl']:
                print('Using private_key: ' + self.config['ssl']['private_key'])
                CherryPyWSGIServer.ssl_private_key = self.config['ssl']['private_key']

    def run(self):
        web.config.log_format = self.config['log_format']
        web.config.log_file = self.config['log_file']
        web.config.log_toprint = False
        web.config.log_tofile = True
        web.config.log_interval = "D" # D=Daily, W0 to rollover every monday
        web.config.log_backups  = 1 # 7 Days?
        arg = "%s:%s" % (self.config['this_host']['host'],self.config['this_host']['port'])
        print "REST: %s" % (arg)
        #sys.argv[1] = [ arg ];
        #sys.argv[1:] = [self.config['this_host']['host'],self.config['this_host']['port']]
        self.app.run(int(self.config['this_host']['port']),WebLog)

class default:

    def GET(self, path):
        # This is the callers IP.
        dip = web.ctx['ip']
        isyhelperRESTObj.helpers.logger.debug('REST:default:GET: ' + dip + ' path='+ path)
        li = path.split("/")
        helper_name = li.pop(0)
        helper = isyhelperRESTObj.helpers.get_helper_by_name(helper_name)
        if not helper:
            msg = "REST:default:GET: No helper '%s' exists from '%s' request by %s" % (helper_name, path, dip)
            isyhelperRESTObj.helpers.logger.error(msg)
            raise web.notfound()
        return helper.rest_get(isyhelperRESTObj.app,li)

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
