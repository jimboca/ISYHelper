#!/usr/bin/python3
#
#
# This code was modeled loosley after:
#  https://github.com/balloob/home-assistant/blob/master/homeassistant/components/device_tracker/ddwrt.py
# And I plan to port it to homeassistant sometime
#
# This can be tested with this address:  http://190.53.26.252/update_clients.asp
#

#<form method="post" name="networkmapdRefresh" action="/apply.cgi" target="hidden_frame">
#<input type="hidden" name="action_mode" value="update_client_list">
#<input type="hidden" name="action_script" value="">
#<input type="hidden" name="action_wait" value="1">
#<input type="hidden" name="current_page" value="httpd_check.xml">
#<input type="hidden" name="next_page" value="httpd_check.xml">
#<input type="hidden" name="client_info_tmp" value="">
#</form>


import re
import requests

class AsusDeviceScanner(object):

    def __init__(self,host,user,password):
        self.host = host
        self.user = user
        self.password = password

    def get_data(self,url):
        try:
            response = requests.get(
                url,
                auth=(self.user,self.password),
                timeout=4
                )
        except requests.exceptions.Timeout:
            print("Connection to the asus router timed out")
            return
        if response.status_code == 200:
            return response.text
        elif response.status_code == 401:
            # Authentication error
            print(
            "Failed to authenticate, "
            "please check your username and password")
            return
        else:
            print("Invalid response from asus: %s", response)

    def logout(self):
        url = 'http://{}/Logout.asp'.format(self.host)
        response = requests.get(
            url,
            auth=(self.user,self.password),
            timeout=4
            )
        print("Logout: "+str(response.status_code))

    def refresh(self):
        url = 'http://{}/apply.cgi?refresh_networkmap'.format(self.host)
        #url = 'http://{}/apply.cgi?update_client_list'.format(self.host)
        response = requests.get(
            url,
            auth=(self.user,self.password),
            timeout=30
            )
        print("Refresh: "+str(response.status_code))

    def client_connected(self,host):
        """Check of host is connected"""
        self.refresh()
        print("client_connected: "+self.host+":"+host)
        url = 'http://{}/update_clients.asp'.format(self.host)
        print("url="+url)
        data = self.get_data(url)
        data.strip().strip("client_list_array = '").strip("';")
        elements = data.split(',')

        aregex = re.compile(r'<[0-9]+>([^>]*)>([^>]*)>([^>]*)>')

        found = False
        for item in elements:
            for name, ip, mac in aregex.findall(item):
                print("name="+name+" ip="+ip+" mac="+mac)
                if host == name:
                    found = True
        self.logout()
        return found
