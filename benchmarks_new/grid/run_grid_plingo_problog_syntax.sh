#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_plingo_problog_${timestamp}.log"
exec >> $logfile

for m in {2..10}
do
    for (( n = 2; n <= $m; n += 1 ))
    do
        echo "START INSTANCE"
        echo "${m} x ${n}"
        plingo plingo_problog_syntax/encoding.lp -q2 -c m=$m -c n=$n --time-limit=1200 2>/dev/null
        echo "EXIT CODE ${?}"
        echo
        done
done



