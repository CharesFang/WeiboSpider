#!/bin/bash

readonly root_dir="$HOME/mongo"

function clean() {
    sudo rm -rf "$root_dir"
}

sudo docker stop weibo
sudo docker rm weibo
clean