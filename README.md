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
   status TINYINT,
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
 INDEX idx_event_id (event_id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE event_participant_tab (
 id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
 created_at INT UNSIGNED NOT NULL,
 updated_at INT UNSIGNED NOT NULL,
 event_id INT UNSIGNED NOT NULL,
 user_id INT UNSIGNED NOT NULL,
 status TINYINT NOT NULL,
 INDEX idx_event_id (event_id)
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

sudo vi /etc/nginx/nginx.conf

# Add these lines to the file:
    server {
        listen 80;
        server_name {YOUR IP OR DOMAIN};
    
        location = /favicon.ico { access_log off; log_not_found off; }
        
        location /static/ {
            autoindex on;
            root /home/khanh/social-event/frontend/build/static;
        }
    
        location /media/ {
            autoindex on;
            alias /var/www/media/;
        }
    
        location /api/ {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://127.0.0.1:8000;
        }
    
        location / {
            proxy_set_header Host $http_host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_pass http://127.0.0.1:5000;
        }
    
    }

    # server {
    #     listen       80 default_server;
    #     listen       [::]:80 default_server;
    #     server_name  _;
    #     root         /usr/share/nginx/html;
    #
    #     # Load configuration files for the default server block.
    #     include /etc/nginx/default.d/*.conf;
    #
    #     location / {
    #     }
    #
    #     error_page 404 /404.html;
    #         location = /40x.html {
    #     }
    #
    #     error_page 500 502 503 504 /50x.html;
    #         location = /50x.html {
    #     }
    # }


server {
    listen 443 http2 ssl;
    listen [::]:443 http2 ssl;

    server_name server_IP_address;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    ########################################################################
    # from https://cipherli.st/                                            #
    # and https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html #
    ########################################################################

    ssl_protocols TLSv1.3;# Requires nginx >= 1.13.0 else use TLSv1.2
    ssl_prefer_server_ciphers on; 
    ssl_dhparam /etc/nginx/dhparam.pem; # openssl dhparam -out /etc/nginx/dhparam.pem 4096
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384;
    ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
    ssl_session_timeout  10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off; # Requires nginx >= 1.5.9
    ssl_stapling on; # Requires nginx >= 1.3.7
    ssl_stapling_verify on; # Requires nginx => 1.3.7
    resolver $DNS-IP-1 $DNS-IP-2 valid=300s;
    resolver_timeout 5s; 
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
                


    ##################################
    # END https://cipherli.st/ BLOCK #
    ##################################

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /media/ {
        autoindex on;
        alias /var/www/media/;
    }

    location /api/ {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:5000;
    }
}


sudo systemcrl restart nginx
```

### Use gunicorn to run your server
```commandline
cd backend/
gunicorn --workers 3 --bind 0.0.0.0:8000 configurations.wsgi
```

# API and Performance
https://docs.google.com/document/d/1j3P-6gAhh_PJnFPoaEaST2mctHyoz8pFvn2etE37ikM/edit?usp=sharing
