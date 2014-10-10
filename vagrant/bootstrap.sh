#!/usr/bin/env bash

#apt-get update
apt-get install python-setuptools
easy_install pip
pip install virtualenv virtualenvwrapper

echo 'Installing environment for Vagrant user'
su - vagrant <<'EOF'
echo `whoami`
mkdir $HOME/virtualenvs
echo 'export WORKON_HOME=$HOME/virtualenvs' >> /home/vagrant/.bash_profile
echo 'export PIP_VIRTUALENV_BASE=$WORKON_HOME' >> /home/vagrant/.bash_profile
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/vagrant/.bash_profile

source /home/vagrant/.bash_profile
mkvirtualenv ban2stats
workon ban2stats
echo 'Basic virtual environment has been setup.'
EOF

#echo 'Installing MaxMind GeoIP from source (required from-source version for Django GeoIP).'
wget -c https://github.com/maxmind/geoip-api-c/releases/download/v1.6.2/GeoIP-1.6.2.tar.gz
tar xvfz GeoIP-1.6.2.tar.gz
cd GeoIP-1.6.2
./configure
make
make install

echo 'Installing Git and Pynalite'
sudo apt-get -y install g++ curl libssl-dev apache2-utils
apt-get -y install git-core
git clone https://github.com/joyent/node.git
cd node
./configure
make
make install

npm install -g dynalite
su - vagrant <<'EOF'
nohup dynalite &
EOF

echo 'Installing Nginx. (For testing Fail2Ban Ban action)'
apt-get -y install nginx


echo 'Installing Fail2Ban.'
apt-get -y install fail2ban
#cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
#Set Fail2Ban Filter for Testing
##echo '[Definition]' >> /etc/fail2ban/filter.d/nginx-http-dev-test.conf
##echo 'failregex = ^<HOST> .*"(GET|POST) .*/login.html.* HTTP.*' >> /etc/fail2ban/filter.d/nginx-http-dev-test.conf
cp /vagrant/jail.local /etc/fail2ban/
cp /vagrant/nginx-http-dev-test.local /etc/fail2ban/filter.d/
cp /vagrant/ban2stats-client.local /etc/fail2ban/action.d/
service fail2ban restart
#See fail2ban log using 'sudo tail -f /var/log/fail2ban.log'


