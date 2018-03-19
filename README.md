# junos-pyez
Network scripts using Junos PyEZ

Set of scripts to learn Junos PyEZ automation.

## pushtemplate.py

Script loads inventory file, template file and variables file. Renders config file from jinja template and pushes it to device/s listed in inventory file.

Directory structure:
1. inventories - folder containing inventory files (.yml) - set of devices and their ip address
1. templates - folder where script is looking for template files (.jinja)
1. variables - folder where script is looking for variables files (.yml)


Required parameters:
1. inventory - name of the inventory file (without extension) located in inventories folder.
1. template - name of the template file (without extension) located in templates folder.
1. variables - name of the variables file (without extension) located in variables folder.

Optional parameters:
1. -dp,--dont-push - skip pushing of config to devices
1. -dg, --dont-generate - skip generating of config
1. -u - username
1. -p - password
1. -t - ticket/Reason/Commit message
1. -ct - config type - set, text or xml
1. -ni - non-interactive processing - yes to all options!! This will automatically commit config.