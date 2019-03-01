#!/bin/bash
# @author: Yampery

if [ $1 == "start" ]; then
    nohup python bin/run.py $2 > logs/console.log 2>&1 &
    echo "$!" > pid
elif [ $1 == "stop" ]; then
    kill `cat pid`
else
    echo "Please use [start, stop]"
fi