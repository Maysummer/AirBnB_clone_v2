#!/usr/bin/env bash
#setup server for deployment
#install nginx ifo not installed
sudo apt -y update
sudo apt -y install nginx

#create folder if not existing (create folders along path)
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared/

#create fake HTML file with dummy content
printf "<html>\n<head></head>\n<body>Hello World!\nThis is a test</body><html>\n" > /data/web_static/releases/test/index.html

#create symbolic link
ln -sf /data/web_static/releases/test/ /data/web_static/current

#change owner and group
chown -R ubuntu:ubuntu /data/

#update config to serve content
new="\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s/^\tlocation \/ {/$new\n\n\tlocation \/ {/" /etc/nginx/sites-enabled/default

sudo service nginx restart
