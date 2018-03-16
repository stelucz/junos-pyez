#!/usr/bin/env python
import argparse
import os
import sys
from funlib import *
from jnpr.junos import Device
import getpass


parser = argparse.ArgumentParser()
parser.add_argument('inventory', help='Name of the inventory file')
parser.add_argument('template', help='Name of the template file')
parser.add_argument('variables', help='Name of the variables file')
parser.add_argument('-dp', '--dont-push', help='Skip pushing of config to devices', action='store_true')
parser.add_argument('-dg', '--dont-generate', help='Skip generating of config', action='store_true')
args, unknown = parser.parse_known_args()

templatePath = os.path.join("templates", args.template + ".jinja")
varsPath = os.path.join("variables", args.variables + ".yml")
inventoryPath = os.path.join("inventories", args.inventory + ".yml")
vars = loadyaml(varsPath)
devices = loadyaml(inventoryPath)
cfgnames = []

if not args.dont_push:
    username = input('Username: ')
    password = getpass.getpass()
    ticket_number = input('Ticket: ')
    print("Config type? \n\t1 - set\n\t2 - text\n\t1 - xml\n\tDefault 1\n")
    choices = {'1': 'set', '2': 'text', '3': 'xml', 'set': 'set', 'text': 'text', 'xml': 'xml'}
    slt = input()
    cfgtype = choices.get(slt, 'set')
i = 0
for dev in devices:
    cfgnames.append(vars['cfg_name'] + "-" + str(i) + '.cfg')
    if not args.dont_generate:
        vars['dev_index'] = i
        config = rendercfg(templatePath, vars)
        savecfg(config, cfgnames[i])
    if not args.dont_push:
        print('You can edit or review configuration file ' + cfgnames[i] + ' before pushing it to device.')
        push = input('Push configs to device ' + dev + ' at ' + devices[dev]['ip'] + ' ? [Y/n]: ')
        if push == '' or push.lower() == 'y':
            cfg = loadconfig(cfgnames[i])
            device = Device(host=devices[dev]['ip'], user=username, passwd=password)
            process_configuration(device, cfg, cfgtype, ticket_number, username)
    i += 1
