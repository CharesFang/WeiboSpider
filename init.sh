#!/bin/bash

# init constant variables

# local machine mongodb dir configures
readonly root_dir="$HOME/mongo"
readonly data_path="$root_dir/data"
readonly config_path="$root_dir/config"
readonly log_path="$root_dir/log"

# mongodb config file
readonly config_name="mongod.conf"

# mongodb log file
readonly log_name="mongod.log"

# mongodb configure file path
readonly config_file_path="$config_path/$config_name"

# mongodb log file path
readonly log_file_path="$log_path/$log_name"

# to initial mongo db dir
function init_dir() {
  if [ ! -d "$root_dir" ]; then
    mkdir "$root_dir" && mkdir "$data_path" && mkdir "$config_path" && mkdir "$log_path"
fi
}


function init_config_file() {

  umask 0111

# create config file
  touch "$config_file_path"

# create log file
  touch "$log_file_path"


# write configures

  cat <<- EOF > "$config_file_path"
processManagement:
   fork: false
net:
   bindIp: 0.0.0.0
   port: 27017
storage:
   dbPath: /data/db
systemLog:
   destination: file
   path: /var/log/mongo/mongod.log
   logAppend: true
storage:
   journal:
      enabled: true
security:
      authorization: enabled
EOF
}


function create_container() {
  sudo docker pull mongo:4.2
  sudo docker run --name weibo --privileged --restart=always  \
  -p 27017:27017 \
  -v $data_path:/data/db \
  -v $log_path:/var/log/mongo \
  -v $config_path:/etc/mongo \
  -d mongo:4.2 -f /etc/mongo/mongod.conf
}

# entry point of program
function main() {
    if [ -d "$root_dir" ]; then
        sudo rm -r "$root_dir"
    fi

    init_dir

    init_config_file

    create_container
}

main

