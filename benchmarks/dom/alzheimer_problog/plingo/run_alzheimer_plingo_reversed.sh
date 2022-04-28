#! /bin/bash

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/alzheimer_plingo_reversed_${timestamp}.log"
exec >> $logfile

for instance in $(ls instances | sort -h)
do
    echo "START INSTANCE"
    echo "${instance}"
    echo "${instance}" >&2
    /usr/bin/time -o $logfile -a plingo instances/${instance} encoding.lp -q2 --time-limit=1200
    echo "EXIT CODE ${?}"
    echo
done
