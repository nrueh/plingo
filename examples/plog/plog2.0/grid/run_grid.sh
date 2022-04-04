#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_${timestamp}.log"
exec >> $logfile

for m in 2 3 4 5 6 7 8 9 10
do
    for n in 2 3 4 5 6 7 8 9 10
    do
        echo
	echo "${m} x ${n}"
	plingo grid.lp --plog -q2 -c m=$m -c n=$n --time-limit=1200 2>/dev/null
    done
done



