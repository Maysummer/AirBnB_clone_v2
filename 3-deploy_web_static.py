#!/usr/bin/python3
"""creates and distributes an archive to your web servers"""

from fabric.api import *
from datetime import datetime
import os

env.hosts = ['3.238.171.60', '3.233.224.138']


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


def do_deploy(archive_path):
    """deploy archive"""
    if not os.path.exists(archive_path):
        return False

    # upload archive to web server
    put(archive_path, "/tmp/")
    # verify / create path on server
    f_name = archive_path.split(".")[0].split("/")[1]
    cmd = "mkdir -p /data/web_static/releases/{}/".format(f_name)
    run(cmd)
    releases = "/data/web_static/releases/{}/".format(f_name)
    # uncompress archive on server
    run("tar -xzf /tmp/{}.tgz -C {}".format(f_name, releases))
    # delete archive on server
    run("rm /tmp/{}.tgz".format(f_name))
    run("mv {}web_static/* {}".format(releases, releases))
    run("rm -rf {}web_static".format(releases))
    # delete symlink
    run("rm -rf /data/web_static/current")
    # create symlink
    run("ln -s {} /data/web_static/current".format(releases))
    return True


def deploy():
    """call do_pack & do_deploy"""
    arc_path = do_pack()
    if not arc_path:
        return False
    val = do_deploy(arc_path)
    return val
