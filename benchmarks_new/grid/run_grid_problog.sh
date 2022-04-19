#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_problog_${timestamp}.log"
exec >> $logfile

for m in {2..10}
do
    for (( n = 2; n <= $m; n += 1 ))
    do
        echo "START INSTANCE"
        echo "${m} x ${n}"
        /usr/bin/time -o $logfile -a problog problog/grid_${m}_${n}.pl --timeout=1200 -v 2>/dev/null
        echo "EXIT CODE ${?}"
        echo
        done
done



