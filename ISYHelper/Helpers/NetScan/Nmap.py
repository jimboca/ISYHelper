"""
Netscan Nmap
"""

import logging
import datetime as dt
from datetime import timedelta
from collections import namedtuple
import subprocess
import re

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

_LOGGER = logging.getLogger(__name__)

Device = namedtuple("Device", ["mac", "name", "ip", "last_update"])

def _arp(ip_address):
    """ Get the MAC address for a given IP. """
    cmd = ['arp', '-n', ip_address]
    arp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, _ = arp.communicate()
    match = re.search(r'(([0-9A-Fa-f]{1,2}\:){5}[0-9A-Fa-f]{1,2})', str(out))
    if match:
        return match.group(0)
    _LOGGER.info("No MAC address found for %s", ip_address)
    return ''


class Nmap(object):
    def __init__(self):
        self.home_interval = 1
        self.last_results = []
        self.hosts = "192.168.1.1-254"

    def scan_devices(self):
        """ Scans for new devices and return a
            list containing found device ids. """

        self._update_info()
        return self.last_results
        return [device.mac for device in self.last_results]

    def get_device_name(self, mac):
        """ Returns the name of the given device or None if we don't know. """

        filter_named = [device.name for device in self.last_results
                        if device.mac == mac]

        if filter_named:
            return filter_named[0]
        else:
            return None

    def _parse_results(self, stdout):
        """ Parses results from an nmap scan.
            Returns True if successful, False otherwise. """
        try:
            results = NmapParser.parse(stdout)
            now = dt.datetime.now()
            self.last_results = []
            for host in results.hosts:
                if host.is_up():
                    if host.hostnames:
                        name = host.hostnames[0]
                    else:
                        name = host.ipv4
                    if host.mac:
                        mac = host.mac
                    else:
                        mac = _arp(host.ipv4)
                    if mac:
                        device = Device(mac.upper(), name, host.ipv4, now)
                        self.last_results.append(device)
            _LOGGER.info("nmap scan successful")
            return True
        except NmapParserException as parse_exc:
            _LOGGER.error("failed to parse nmap results: %s", parse_exc.msg)
            self.last_results = []
            return False

    def _update_info(self):
        """ Scans the network for devices.
            Returns boolean if scanning successful. """
        #if not self.success_init:
        #    return False

        _LOGGER.info("Scanning")

        options = "-F --host-timeout 5"
        exclude_targets = set()
        if self.home_interval:
            now = dt.datetime.now()
            for host in self.last_results:
                if host.last_update + self.home_interval > now:
                    exclude_targets.add(host)
            if len(exclude_targets) > 0:
                target_list = [t.ip for t in exclude_targets]
                options += " --exclude {}".format(",".join(target_list))

        nmap = NmapProcess(targets=self.hosts, options=options)

        nmap.run()

        if nmap.rc == 0:
            if self._parse_results(nmap.stdout):
                self.last_results.extend(exclude_targets)
        else:
            self.last_results = []
            _LOGGER.error(nmap.stderr)
            return False

if __name__ == "__main__":
    mobj = NetscanNmap()
    devs = mobj.scan_devices()
    print(devs)
    for device in devs:
        print("mac="+device.mac+" name="+device.name+" ip="+device.ip)
