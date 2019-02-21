sudo apt-get install -y software-properties-common
sudo add-apt-repository ppa:jonathonf/ffmpeg-4
sudo add-apt-repository universe
sudo add-apt-repository ppa:certbot/certbot
sudo apt-get update

sudo apt-get install -y python3 python3-pip ffmpeg nginx git postgresql postgresql-contrib golang-go libssl-dev certbot

sudo service nginx stop
sudo certbot certonly --standalone -d vidsocial.org -d www.vidsocial.org

sudo -u postgres psql -c "create database ipfs_db5"
sudo -u postgres psql -c "create user ipfs with encrypted password 'ipfs@pranish'"
sudo -u postgres psql -c "grant all privileges on database ipfs_db5 to ipfs"

ssh-keygen -t rsa -b 4096 -C "n00bdan13@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub

wget https://dist.ipfs.io/go-ipfs/v0.4.18/go-ipfs_v0.4.18_linux-amd64.tar.gz
tar xvfz go-ipfs_v0.4.18_linux-amd64.tar.gz
go-ipfs/install.sh
ipfs init
nohup ipfs daemon &

wget https://github.com/ant-media/Ant-Media-Server/releases/download/release-1.6.1/ant-media-server-1.6.1-community-1.6.1-190108_1656.zip
wget https://raw.githubusercontent.com/ant-media/Scripts/master/install_ant-media-server.sh
chmod 755 install_ant-media-server.sh
sudo ./install_ant-media-server.sh ant-media-server*.zip
sudo /usr/local/antmedia/enable_ssl.sh -d stream.vidsocial.org

python3 -m pip install -r requirements.txt
#nginx config