#!/usr/bin/python3
"""generates a .tgz archive from contents of web_static"""

from fabric.api import *
from datetime import datetime


def do_pack():
    """function to archive"""
    local("mkdir -p versions")
    arcName = "web_static_{}.tgz".format(datetime.strftime(datetime.now(),
                                                           "%Y%m%d%H%M%S"))
    path = "versions/" + arcName
    cmd = "tar -cvzf " + path + " web_static"
    res = local(cmd)
    if res.succeeded:
        return path
    else:
        return None
