#! /bin/bash

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

export logfile="logs/grid_plingo_optenum_timeout_${timestamp}.log"
exec >> $logfile


for m in {6..9}
do
    case $m in
        6)
            min_n=5
            ;;
        7)
            min_n=4
            ;;
        8)
            min_n=4
            ;;
        9)
            min_n=3
            ;;
        *)
            continue
            ;;
    esac
    for (( n = $min_n; n <= $m; n += 1 ))
    do
        echo "START INSTANCE"
        echo "${m} x ${n}"
        echo "${m} x ${n}" >&2
        plingo plingo/encoding.lp plingo/grid_${m}_${n}.lp --plog -q2 -c m=$m -c n=$n --opt-enum --time-limit=1200 2>/dev/null
        echo "EXIT CODE ${?}"
        echo
    done
done

sed -i.backup '/Solving.../ d' $logfile


