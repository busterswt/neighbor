#! /usr/bin/python3

# Returns a json blob with CDP/LLDP information from server neighbors
# james.denton@rackspace.com

import json
import time
from pyroute2 import NDB
from pyroute2 import IPRoute
from retry import retry
from scapy.all import *

ipr = IPRoute()
ndb = NDB(log='DEBUG')

# CDP defaults to 60s
# LLDP defaults to 30s
listen_timeout = 121

# We will want to:
# 1. Check only REAL interfaces (i.e. eth)
# 2. Check only UP interfaces
# 3. Check CDP first
# 4. Fallback to LLDP
# 5. Timeout if necessary

@retry(Exception, tries=3, delay=2)
def get_interface_neighbors(iface):

    # Get interface state
    state = ipr.get_links(ipr.link_lookup(ifname=iface['ifname']))[0].get_attr('IFLA_OPERSTATE')
    interface_dict[iface['ifname']] = {}
    try:
        if state == 'UP':
            ##print('Listening for CDP and LLDP...')
            p = sniff(timeout=listen_timeout, iface=iface['ifname'], count=1, filter="(ether[20:2] == 0x2000 or ether proto 0x88cc) and inbound")

            try:
                neighbor = p[0]["CDPMsgDeviceID"].val.decode()
                platform = p[0]["CDPMsgPlatform"].val.decode()
                switchport = p[0]["CDPMsgPortID"].iface.decode()

                interface_dict[iface['ifname']]['protocol'] = "CDP"
                interface_dict[iface['ifname']]['neighbor'] = neighbor
                interface_dict[iface['ifname']]['platform'] = platform
                interface_dict[iface['ifname']]['switchport'] = switchport
                interface_dict[iface['ifname']]['state'] = state
                ##print('CDP packet arrived on %s ' % (iface['ifname']))
            except:
                neighbor = p[0]["LLDPDUSystemName"].system_name.decode()
                platform = "n/a"
                switchport = p[0]["LLDPDUPortID"].id.decode()

                interface_dict[iface['ifname']]['protocol'] = "LLDP"
                interface_dict[iface['ifname']]['neighbor'] = neighbor
                interface_dict[iface['ifname']]['platform'] = platform
                interface_dict[iface['ifname']]['switchport'] = switchport
                interface_dict[iface['ifname']]['state'] = state
                ##print('LLDP packet arrived on %s ' % (iface['ifname']))

    except Exception as e:
        ##print('%s - CDP/LLDP timeout on %s. No response' % (e,iface['ifname']))
        interface_dict[iface['ifname']]['protocol'] = "timeout"
        interface_dict[iface['ifname']]['neighbor'] = "timeout"
        interface_dict[iface['ifname']]['platform'] = "timeout"
        interface_dict[iface['ifname']]['switchport'] = "timeout"
        interface_dict[iface['ifname']]['state'] = state

if __name__ == '__main__':
    # Load scapy CDP/LLDP libraries
    load_contrib("cdp")
    load_contrib("lldp")

    # Grab ALL interfaces
    ifaces = json.loads(str(ndb .interfaces .dump() .select('index', 'ifname', 'kind') .format('json')))

    interface_dict = {}
    for iface in ifaces:
        # Limit to REAL interfaces (i.e. ethernet)
        if iface['kind'] not in ['veth','bridge','vxlan','bond','vlan']:
            get_interface_neighbors(iface=iface)

    print(json.dumps(interface_dict))
