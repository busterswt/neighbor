#! /usr/bin/python3

# Returns a json blob with CDP/LLDP information from server neighbors
# james.denton@rackspace.com

import argparse
import csv
import json
import socket
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
            print('Listening for CDP and LLDP on %s...' % (iface['ifname']))
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
                print('CDP packet arrived on %s ' % (iface['ifname']))
            except:
                neighbor = p[0]["LLDPDUSystemName"].system_name.decode()
                platform = "n/a"
                switchport = p[0]["LLDPDUPortID"].id.decode()

                interface_dict[iface['ifname']]['protocol'] = "LLDP"
                interface_dict[iface['ifname']]['neighbor'] = neighbor
                interface_dict[iface['ifname']]['platform'] = platform
                interface_dict[iface['ifname']]['switchport'] = switchport
                interface_dict[iface['ifname']]['state'] = state
                print('LLDP packet arrived on %s ' % (iface['ifname']))
        elif state == 'DOWN':
            print('Interface %s is DOWN. Skipping!' % (iface['ifname']))

    except Exception as e:
        print('%s - CDP/LLDP timeout or unexpected packet on %s.' % (e,iface['ifname']))
        interface_dict[iface['ifname']]['protocol'] = "timeout"
        interface_dict[iface['ifname']]['neighbor'] = "timeout"
        interface_dict[iface['ifname']]['platform'] = "timeout"
        interface_dict[iface['ifname']]['switchport'] = "timeout"
        interface_dict[iface['ifname']]['state'] = state

def write_csv(filename, interface_dict):
    # field names
    fields = ['hostname', 'interface', 'protocol', 'neighbor', 'platform', 'switchport', 'state']

    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        csvwriter.writerow(fields)

        for iface, neigh in interface_dict.items():
            if neigh:
                row = [str(socket.gethostname()),
                       str(iface),
                       str(neigh['protocol']),
                       str(neigh['neighbor']),
                       str(neigh['platform']),
                       str(neigh['switchport']),
                       str(neigh['state'])]
                csvwriter.writerow(row)

    csvfile.close()

def write_json(filename, interface_dict):
    with open(filename, 'w') as jsonfile:
        json.dump(interface_dict, jsonfile)

    jsonfile.close()

if __name__ == '__main__':
    print("\nHello, neighbor!\r\n")

    parser = argparse.ArgumentParser(description="Grab CDP/LLDP neighbor information")
    #group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument("--csv", default=False, action="store_true", help="Provides output in csv format")
    parser.add_argument("--json", default=True, action="store_true", help="Provides output in json format")
    args = parser.parse_args()

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

##    print(json.dumps(interface_dict, indent=4, sort_keys=True))

    # Write to file(s) for further parsing (defaults to JSON)
    if args.csv:
        filename = "%s_neighbors.csv" % (socket.gethostname())
        write_csv(filename, interface_dict)
        print('### Output written to %s ###' % filename)

    if args.json and not args.csv:
        filename = "%s_neighbors.json" % (socket.gethostname())
        write_json(filename, interface_dict)
        print('### Output written to %s ###' % filename)
