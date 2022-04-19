#! /bin/bash
export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_plingo_unsat_${timestamp}.log"
exec >> $logfile

for m in {2..9}
do
    for (( n = 2; n <= $m; n += 1 ))
    do
        echo "START INSTANCE"
        echo "${m} x ${n}"
        echo "${m} x ${n}" >&2
        plingo plingo/encoding.lp plingo/grid_${m}_${n}.lp --plog -q2 --unsat -c m=$m -c n=$n --time-limit=1200 2>/dev/null
        echo "EXIT CODE ${?}"
        echo
        done
done


