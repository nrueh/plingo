#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_plog2_${timestamp}.log"
exec >> $logfile

for m in {2..9}
do
    for (( n = 2; n <= $m; n += 1 ))
    do
        echo "START INSTANCE"
        echo "${m} x ${n}"
        /usr/bin/time -o $logfile -a timeout 1200 ./plog2 plog2.0/grid_${m}_${n}.plog
        echo "EXIT CODE ${?}"
        echo
        done
done

