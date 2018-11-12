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

### Install mysqlclient
```commandline
sudo apt-get install python-dev default-libmysqlclient-dev
pip install mysqlclient
```

# Database schema
```mysql
CREATE DATABASE social_event_db;

USE social_event_db;

CREATE TABLE user_tab (
   id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
   created_at INT UNSIGNED NOT NULL,
   updated_at INT UNSIGNED NOT NULL,
   fullname VARCHAR(20),
   sex TINYINT,
   date_of_birth INT UNSIGNED,
   username VARCHAR(20) NOT NULL UNIQUE,
   avatar_path VARCHAR(100) NOT NULL,
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
   location_name VARCHAR(100),
   location_x DECIMAL,
   location_y DECIMAL,
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