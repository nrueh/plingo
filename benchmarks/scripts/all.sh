#./scripts/run_bm.sh plingo birds
#./scripts/run_bm.sh problog birds
#./scripts/run_bm.sh azreasoners birds


# Grid benchmark
# TODO: There are two encodings for plingo grid (P-log and Problog syntax). Add both
./script/run_bm.sh plingo grid exact plog # plog should be transformed to option --plog

./script/run_bm.sh plog grid exact
./script/run_bm.sh plog-dco grid exact
./script/run_bm.sh problog grid exact

./script/run_bm.sh plingo grid sample plog # Default sample mode is timeout
./script/run_bm.sh plingo grid sample balanced10 plog # balanced10 should be transformed to option -b10
./script/run_bm.sh plingo grid sample balanced100 plog # the extra arguments can be used to uniquely name the results
./script/run_bm.sh plingo grid sample balanced1000 plog
./script/run_bm.sh plingo grid sample balanced10000 plog
./script/run_bm.sh plingo grid sample balanced100000 plog
./script/run_bm.sh plingo grid sample balanced1000000 plog
./script/run_bm.sh plingo grid sample balanced10000000 plog

# Other P-Log benchmarks
./script/run_bm.sh plingo nasa exact plog 
./script/run_bm.sh plingo squirrel exact plog
./script/run_bm.sh plingo blocks exact plog

./script/run_bm.sh plog nasa exact
./script/run_bm.sh plog squirrel exact
./script/run_bm.sh plog blocks exact

./script/run_bm.sh plog-dco nasa exact
./script/run_bm.sh plog-dco squirrel exact
./script/run_bm.sh plog-dco blocks exact

# LPMLN benchmarks
./scripts/run_bm.sh plingo alzheimer_problog mpe
./scripts/run_bm.sh plingo alzheimer_problog mpe unsat # unsat should be transformed to --unsat
./scripts/run_bm.sh azreasoners alzheimer_problog mpe

./scripts/run_bm.sh plingo smokers mpe
./scripts/run_bm.sh plingo smokers mpe unsat
./scripts/run_bm.sh azreasoners smokers mpe
