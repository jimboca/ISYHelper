"""
IFTTT Maker Helper
"""

from .Helper import Helper
import json

class Maker(Helper):

    def __init__(self,parent,hconfig):
        self.required = ['token']
        super(Maker, self).__init__(parent,hconfig)

    def maker(self,path,data):
        #super(Tester, self).setvar(name,value)
        lpfx = self.name + ".maker: "
        self.parent.logger.info(lpfx + ' path=' + path + ' data=' + data)
        jdata = json.loads(data)
        self.parent.logger.info(lpfx + ' jdata=' + repr(jdata))
        errors = 0
        for key in ['token','type','name','value']:
            if not key in jdata:
                self.parent.logger.error(lpfx + 'Missing key: ' + key)
                errors += 1
        if errors > 0:
            raise ValueError("Missing Keys")
            return
        if not jdata['token'] == self.token:
            self.parent.logger.error(lpfx + 'Token mismatch ' + jdata['token'] + ' != ' + self.token)
            return
        if jdata['type'] == 'variable':
            var = self.setvar(jdata['name'],jdata['value']);
        else:
            self.parent.logger.error(lpfx + 'Unknown type: ' + jdata['type'])
