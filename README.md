# Installation
- You need to install MySQL first

- Install some python packages
```commandline
# Install virtualenvwrapper
sudo pip install virtualenvwrapper
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
echo "source /usr/local/bin/virtualenvwrapper.sh" > ~/.bashrc
mkvirtualenv mysite
workon mysite

# Install Python dependency
sudo pip install -r requirements.txt
```

- Default settings is from file `local.py`. If you want to change, please run those commands:
```commandline
python manage.py runserver --settings=mysite.settings.development
python manage.py migrate --settings=mysite.settings.production
``` 

