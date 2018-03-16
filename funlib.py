import sys
import yaml
import getpass
from jinja2 import Template
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import ConnectAuthError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import UnlockError
from jnpr.junos.exception import ConfigLoadError
from jnpr.junos.exception import CommitError


def loadyaml(path):
    with open(path) as f:
        vars = f.read()
    return yaml.load(vars)


def loadconfig(path):
    with open(path) as f:
        conf = f.read()
    return conf


def rendercfg(jipath, vars):
    print("\nGenerating configuration...")
    with open(jipath) as f:
        s = f.read()
        template = Template(s)
    return template.render(vars)


def savecfg(config, path):
    print("\nSaving configuration.")
    with open(path, "w") as f:
        f.write(config)


def open_device(dev):
    connected = False
    unreachable = False
    attempt = 0
    while not(connected or unreachable or attempt > 2):
        attempt += 1
        try:
            dev.open()
            dev.timeout = 60
            connected = True
        except ConnectAuthError as err:
            print("Cannot authenticate: {}".format(err))
            password = getpass.getpass(prompt='Password: ', stream=None)
            dev.password = password
        except ConnectError as err:
            print("Cannot connect to the device: {}".format(err))
            unreachable = True
    return connected


def lock_configuration(dev):
    # Lock device configuration
    locked = False
    print("Locking the configuration")
    with Config(dev) as cu:
        cu.lock()
        locked = True
        return locked


def push_config(dev, config, format):
    assert format in ["set", "xml", "text"]
    with Config(dev) as cu:
        cu.load(config, format=format)
        changes = cu.diff()
        return changes


def commit_configuration(dev, ticket, username):
    print("Committing the configuration")
    with Config(dev) as cu:
        commited = cu.commit(comment=ticket + " / " + username)
        cu.unlock()
        return commited


def rollback_configuration(dev):
    print("Discarding changes")
    with Config(dev) as cu:
        cu.rollback()
        cu.unlock()


def process_configuration(dev, config, format, ticket_number, user):
    if open_device(dev):
        lock_configuration(dev)
        print(push_config(dev, config, format))
        cmt = input('Commit changes? [Y/n]: ')
        if cmt == '' or cmt.lower() == 'y':
            commit_configuration(dev, ticket_number, user)
        else:
            rollback_configuration(dev)
