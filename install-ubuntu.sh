#! /bin/sh

#install dependencies
pip3 install youtube_dl

#install server
sudo mkdir /opt/youtube-mpv
sudo cp ytdl_server.py /opt/youtube-mpv/
sudo cp ytdl_config.py /opt/youtube-mpv/

#install DAEMON

#replace with your user
sed -i -e 's/--chuid USERNAME/--chuid '`whoami`'/g' daemon
sudo cp daemon /etc/init.d/youtube-mpv
sudo chmod +x /etc/init.d/youtube-mpv

#run service
#!!warning service should not be started as:
#`service youtube-mpv start`
#instead you should manually run as full path
sudo /etc/init.d/youtube-mpv start

