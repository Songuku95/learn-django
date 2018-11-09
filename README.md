# Social Event - Entry Task

## Installation
### Install MySQL
```commandline
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo mysql
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123';
```

### Install virtualenvwrapper
```commandline
sudo pip install virtualenvwrapper
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
echo "source /usr/local/bin/virtualenvwrapper.sh" > ~/.bashrc
mkvirtualenv social_event
workon social_event
```