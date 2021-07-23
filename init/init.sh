#!/bin/bash

# init constant variables

# local machine mongodb dir configures
readonly root_dir="$HOME/mongo"
readonly data_path="$root_dir/data"
readonly config_path="$root_dir/config"
readonly log_path="$root_dir/log"
readonly resource_path="$root_dir/resource"

# mongodb config file
readonly config_name="mongod.conf"

# mongodb log file
readonly log_name="mongod.log"

# mongodb init scripts
readonly db_file_name="db_init.js"

# mongodb configure file path
readonly config_file_path="$config_path/$config_name"

# mongodb log file path
readonly log_file_path="$log_path/$log_name"

# to initial mongo db dir
function init_dir() {
  if [ ! -d "$root_dir" ]; then
    mkdir "$root_dir" && mkdir "$data_path" && mkdir "$config_path" && mkdir "$log_path" && mkdir "$resource_path"
fi
}


function init_file() {

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

#  create mongo database init json file
  cp "$(pwd)/init/resource/$db_file_name" "$resource_path"
  sudo chmod 755 "$resource_path/$db_file_name"
}


function create_container() {
#  sudo docker pull mongo:4.2
  sudo docker run --name weibo --privileged --restart=always  \
  -p 27017:27017 \
  -v "$data_path":/data/db \
  -v "$log_path":/var/log/mongo \
  -v "$config_path":/etc/mongo \
  -v "$resource_path":/etc/resource \
  -d mongo:4.2 -f /etc/mongo/mongod.conf
}

# entry point of program
function main() {
  if [ -d "$root_dir" ]; then
    sudo rm -r "$root_dir"
  fi

# to create mongodb work dir
  init_dir
  echo "MongoDB work dir initialized."

# to create mongodb config file, log file and database initial script.
  init_file
  echo "MongoDB running files created."

# to create and start mongodb docker container
  create_container
  echo "MongoDB container created."

  cat <<- EOF
Run CMD:
  "sudo docker exec -it weibo mongo 127.0.0.1:27017 /etc/resource/db_init.js"
to initial Database.
EOF

}

main

