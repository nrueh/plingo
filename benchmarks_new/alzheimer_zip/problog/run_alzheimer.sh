#! /bin/bash

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/alzheimer_problog_${timestamp}.log"
exec >> $logfile

for instance in $(ls instances | sort -h)
do
    for query in $(ls queries)
    do
        echo "START INSTANCE"
        echo "${instance} ${query}"
        cat instances/${instance} > instance.pl
        cat queries/${query} >> instance.pl
        /usr/bin/time -o $logfile -a problog instance.pl -v --timeout=1200
        echo "EXIT CODE ${?}"
        echo
    done
done

if [[ -f instance.pl ]]
then
    rm instance.pl
fi
