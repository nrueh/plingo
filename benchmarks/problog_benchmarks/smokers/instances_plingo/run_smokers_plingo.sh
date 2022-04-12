#! /bin/bash

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/smokers_plingo_${timestamp}.log"
exec >> $logfile

for instance in $(ls instances | sort -h)
do
    echo "START INSTANCE"
    echo "${instance}"
    echo "${instance}" >&2
    /usr/bin/time -o $logfile -a plingo encoding.lp instances/${instance} -q2 --time-limit=1200
    echo "EXIT CODE ${?}"
    echo
done
