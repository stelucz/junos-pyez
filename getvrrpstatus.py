#!/usr/bin/env python
import argparse
import os
import sys
from funlib import *
from jnpr.junos import Device
import getpass
from cfg_tables.bgp.bgpsummary import BgpSummaryTable
from prettytable import PrettyTable


parser = argparse.ArgumentParser()
parser.add_argument('inventory', help='Name of the inventory file')
# parser.add_argument('template', help='Name of the template file')
# parser.add_argument('variables', help='Name of the variables file')
parser.add_argument('-u', help='Username')
parser.add_argument('-p', help='Password')
parser.add_argument('-f', help='Full output', action='store_true')
parser.add_argument('-s', help='Show summary table', action='store_true')
args, unknown = parser.parse_known_args()

inventoryPath = os.path.join("inventories", args.inventory + ".yml")
devices = loadyaml(inventoryPath)


if not args.u:
    username = input('Username: ')
else:
    username = args.u
if not args.p:
    password = getpass.getpass()
else:
    password = args.p


outputtable = PrettyTable(['Device', 'Peer', 'State', 'Description', 'Peer AS', 'Elapsed Time'])

for dev in sorted(devices):
    device = Device(host=devices[dev]['ip'], user=username, passwd=password)
    open_device(device)
    tbl = BgpSummaryTable(device).get()
    for peer in tbl:
        # print(peer.bgp_rib.items())
        if peer.peer_state != 'Established':
            outputtable.add_row([dev, peer.peer_address, peer.peer_state, peer.description, peer.peer_as,
                                 peer.elapsed_time])
        elif args.f or args.s:
            outputtable.add_row([dev, peer.peer_address, peer.peer_state, peer.description, peer.peer_as,
                                 peer.elapsed_time])
    if args.f:
        for peer in tbl:
                ribtable = PrettyTable(['Device', 'Peer', 'Description', 'RIB name', 'Received prefixes',
                                        'Accepted prefixes'])
                for rib in peer.rib:
                    ribtable.add_row([dev, peer.peer_address, peer.description, rib.name, rib.received_prefix,
                                      rib.accepted_prefix])
                print(ribtable)

if not args.f:
    if outputtable.__getattr__("rowcount") > 0 or args.s:
        print(outputtable)
    else:
        print('No peers in non-Established state')
else:
    print(outputtable)

print('Script finished')
