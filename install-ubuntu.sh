#! /bin/sh

me=`whoami`
install_path=/opt/youtube-mpv/

#install dependencies
pip3 install youtube_dl

#install server
sudo mkdir /opt/youtube-mpv
sudo cp ytdl_server.py $install_path
sudo cp ytdl_config.py $install_path
sudo cp ytdl_db.py $install_path
sudo cp history.db $install_path
sudo chown -R $me:$me $install_path 
sudo chmod -R 755 $install_path

#install DAEMON

#replace with your user
sed -i -e 's/--chuid USERNAME/--chuid '$me'/g' daemon
sudo cp daemon /etc/init.d/youtube-mpv
sudo chmod +x /etc/init.d/youtube-mpv

#run service
#!!warning service should not be started as:
#`service youtube-mpv start`
#instead you should manually run as full path
sudo /etc/init.d/youtube-mpv start

#run daemon at startup
sudo systemctl enable youtube-mpv
