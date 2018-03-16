# junos-pyez
Network scripts using Junos PyEZ

Set of scripts to learn Junos PyEZ automation.

## pushtemplate.py

Script loads inventory file, template file and variables file. Renders config file from jinja template and pushes it to device/s listed in inventory file.

Required parameters:
1. inventory - name of the inventory file (without extension) located in inventories folder.
1. template - name of the template file (without extension) located in templates folder.
1. variables - name of the variables file (without extension) located in variables folder.

Optional parameters:
1. -dp,--dont-push - skip pushing of config to devices
1. -dg, --dont-generate - skip generating of config