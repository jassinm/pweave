from fabric.api import local


def install():
    """docstring for in"""
    local('sudo python setup.py install')
    local('mkdir -p $HOME/.pweave_plugins')
    local('cp -r ./pweave/pweave_plugins/* $HOME/.pweave_plugins/')
