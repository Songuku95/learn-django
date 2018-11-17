# Social Event - Entry Task

## Installation

### Install MySQL
```commandline
sudo yum update
yum install wget
wget http://repo.mysql.com/mysql80-community-release-el7-1.noarch.rpm
sudo rpm -ivh mysql80-community-release-el7-1.noarch.rpm
yum update
sudo yum install mysql-server
sudo systemctl start mysqld
```

### Config MySQL
```commandline
# Get temporary password
sudo grep 'temporary password' /var/log/mysqld.log
sudo mysql_secure_installation

# Change password for root user
mysql -u root -p
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Y0ur_P@ssword';
```

### Install pip
```commandline
sudo yum install epel-release
sudo yum install python-pip
sudo pip install --upgrade pip

# Check pip version
pip --version
```

### Install virtualenvwrapper
```commandline
sudo pip install virtualenvwrapper
export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
echo "export WORKON_HOME=~/Envs" >> ~/.bashrc
echo "source /usr/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv social_event
workon social_event
```

### Clone project
```commandline
# Install some necessary packages
sudo yum -y install gcc gcc-c++ kernel-devel
sudo yum -y install python-devel libxslt-devel libffi-devel openssl-devel
sudo yum -y install git python-devel mysql-devel

# Clone project
git clone https://git.ved.com.vn/EntryTask/duykhanh.nguyen.git

# Change folder name
mv duykhanh.nguyen/ social-event/

# Switch to `dev` branch
cd social-event/
git checkout dev
```

### Install backend
```commandline
cd backend/
pip install -r requirements.txt
```

### Create database
```mysql
CREATE DATABASE social_event_db;

USE social_event_db;

CREATE TABLE user_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,
   email VARCHAR(100) NOT NULL,
   fullname VARCHAR(20),
   sex TINYINT,
   username VARCHAR(20) NOT NULL UNIQUE,
   avatar_path VARCHAR(100),
   password_hash VARCHAR(100) NOT NULL,
   password_salt VARCHAR(100) NOT NULL,
   role TINYINT
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,   
   user_id INT UNSIGNED NOT NULL,
   title VARCHAR(20) NOT NULL,
   description VARCHAR(10000) NOT NULL,
   start_date INT UNSIGNED NOT NULL,
   end_date INT UNSIGNED NOT NULL,
   address VARCHAR(100),
   latitude DECIMAL,
   longitude DECIMAL,
   status TINYINT
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE image_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,
   path VARCHAR(200),
   event_id INT UNSIGNED NOT NULL,
   status TINYINT,
   INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE comment_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 content VARCHAR(10000),
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status TINYINT,
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_liker_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status INT,
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_participant_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status TINYINT,
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE tag_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(20),
 INDEX idx_name_id (name)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_category_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 tag_id INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Install frontend
```commandline
cd frontend/
curl -sL https://rpm.nodesource.com/setup_10.x | sudo bash -
sudo yum install nodejs
npm install
```


## Deployment

### Install nginx
```commandline
sudo yum install nginx

sudo vi /etc/nginx/nginx.conf

# Add these lines:
server {
    listen 80;
    server_name {YOUR IP OR DOMAIN};

    location = /favicon.ico { access_log off; log_not_found off; }


    location /media/ {
        root /home/khanh/social-event/backend;
    }

    location /api/ {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}

sudo systemcrl restart nginx
```

### Use gunicorn to run your server
```commandline
cd backend/
gunicorn --workers 3 --bind 0.0.0.0:8000 configurations.wsgi
```