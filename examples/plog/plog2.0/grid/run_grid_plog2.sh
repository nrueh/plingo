#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_plog2_${timestamp}.log"
exec >> $logfile

for m in 2 3 4 5
do
    for n in 2 3 4 5 6 7 8 9 10
    do
        echo
	echo "${m} x ${n}"
	/usr/bin/time -o $logfile -a timeout 1200 ./plog2 original/Grid/grid_${m}_${n}.plog
    done
done

