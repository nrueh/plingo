#! /bin/bash

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/alzheimer_lpmln_${timestamp}.log"
exec >> $logfile

for instance in $(ls instances | sort -h)
do
    echo "START INSTANCE"
    echo "${instance}"
    echo "${instance}" >&2
    /usr/bin/time -o $logfile -a timeout 1200 lpmln-infer encoding.lp show.lp instances/${instance} -v 1 -timeout=1200
    echo "EXIT CODE ${?}"
    echo
done

if [[ -f asp.pl ]]
then
    rm asp.pl
fi
