#!/bin/bash

# init constant variables

# mongodb config file
config_name="mongod.conf"

# mongodb log file
log_name="mongod.log"

# local machine mongodb dir configures
root_dir="$HOME/mongo"
data_path="$root_dir/data"
config_path="$root_dir/config"
log_path="$root_dir/log"


# to initial mongo db dir
function init_dir() {
  if [ ! -d "$root_dir" ]; then
  mkdir "$root_dir"
  mkdir "$data_path"
  mkdir "$config_path"
  mkdir "$log_path"
fi
}


function init_config_file() {
  config_file_path="$config_path/$config_name"
  if [ -e "$config_file_path" ]; then
      rm "$config_file_path"
  fi
  touch "$config_file_path"
  cat _EOF_ > "$config_file_path"

  _EOF_
}




