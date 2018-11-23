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

### Install redis
```commandline
sudo yum install redis
sudo systemctl start redis
sudo systemctl enable redis
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
   fullname VARCHAR(20),
   sex TINYINT,
   email VARCHAR(50) NOT NULL,
   username VARCHAR(20) NOT NULL UNIQUE,
   avatar_path VARCHAR(100),
   password_hash VARCHAR(200) NOT NULL,
   password_salt VARCHAR(100) NOT NULL,
   role TINYINT
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,   
   user_id INT UNSIGNED NOT NULL,
   title VARCHAR(100) NOT NULL,
   description VARCHAR(10000) NOT NULL,
   start_date INT UNSIGNED NOT NULL,
   end_date INT UNSIGNED NOT NULL,
   address VARCHAR(200),
   latitude DECIMAL,
   longitude DECIMAL,
   status TINYINT
   INDEX idx_start_date_end_date (start_date, end_date)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE image_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,
   path VARCHAR(200) NOT NULL,
   event_id INT UNSIGNED NOT NULL,
   status TINYINT NOT NULL,
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
 status TINYINT NOT NULL,
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_liker_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status INT NOT NULL,
 INDEX idx_event_id_user_id (event_id, user_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_participant_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status TINYINT NOT NULL,
 INDEX idx_event_id_user_id (event_id, user_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE tag_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 name VARCHAR(20) NOT NULL,
 INDEX idx_name (name)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_tag_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 tag_id INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 INDEX idx_event_id_tag_id (event_id, tag_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE INDEX idx_username ON user_tab (username); 
CREATE INDEX idx_email ON user_tab (email);
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
sudo systemctl start nginx
sudo systemctl enable nginx

# Create SSL Certificate
sudo mkdir /etc/ssl/private
sudo chmod 700 /etc/ssl/private
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-on-centos-7
```

### Use gunicorn to run your server
```commandline
cd backends/
gunicorn --workers 4 --bind 0.0.0.0:8000 member.wsgi
gunicorn --workers 4 --bind 0.0.0.0:9000 admin.wsgi
```

# API and Performance
https://docs.google.com/document/d/1j3P-6gAhh_PJnFPoaEaST2mctHyoz8pFvn2etE37ikM/edit?usp=sharing
