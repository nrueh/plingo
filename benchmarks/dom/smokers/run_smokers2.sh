#! /bin/bash

read -p "Are you in the correct env?"

export timestamp=$(date +%s)

if [[ ! -d logs ]]
then
    mkdir logs
fi

if [ "$1" == "plingo" ] && [ "$2" == "unsat" ]
then
    additional="_unsat"
    options="--unsat "
fi

export logfile="logs/smokers2_${1}${additional}_${timestamp}.log"
exec >> $logfile


if [ ! -z "$1" ]
then
    case $1 in 
        plingo)
            command="/usr/bin/time -o $logfile -a plingo plingo_encoding.lp"
            options+="-q2 --time-limit=1200"
            ;;
        lpmln)
            command="/usr/bin/time -o $logfile -a timeout 1200 lpmln-infer lpmln_encoding.lp"
            options=" -v 1 -timeout=1200"
            ;;
        problog)
            echo "No command available for Problog yet"
            exit 1
            ;;
        *)
            echo "First argument has to be name of system: plingo, lpmln or problog" >&2
            exit 1
            ;;
    esac
else
    echo "No system specified: plingo, lpmln or problog" >&2
    exit 1
fi 



for instance in $(ls instances | sort -V)
do
    echo "START INSTANCE"
    echo "${instance}"
    echo "${instance}" >&2
    $command instances/$instance $options
    echo "EXIT CODE ${?}"
    echo
done

if [[ -f asp.pl ]]
then
    rm asp.pl
fi

# Clean up lpmln logfile, remove empty Answer Set Lines
if [ "$1" == "lpmln" ]
then
    sed -i.backup '/Answer:/,+2 d' $logfile
fi
