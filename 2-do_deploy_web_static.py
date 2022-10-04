#!/usr/bin/python3
"""distributes an archive to your web servers, using the function do_deploy"""

from fabric.api import *
import os


env.hosts = ['3.238.171.60', '3.233.224.138']


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
    run("rm /tmp/{}.tgz".f_name)
    run("mv {}web_static/* {}".format(releases, releases))
    run("rm -rf {}web_static".format(releases))
    # delete symlink
    run("rm -rf /data/web_static/current")
    # create symlink
    run("ln -s {} /data/web_static/current".format(releases))
    return True
