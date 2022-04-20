#./scripts/run_bm.sh plingo birds
#./scripts/run_bm.sh problog birds
#./scripts/run_bm.sh azreasoners birds


# Grid benchmark
# TODO: There are two encodings for plingo grid (P-log and Problog syntax). Add both
./script/run_bm.sh bm_plog plingo grid exact '--plog' # plog should be transformed to option --plog

./script/run_bm.sh bm_normal plog grid exact
./script/run_bm.sh bm plog-dco grid exact
./script/run_bm.sh bm problog grid exact

./script/run_bm.sh bm_defaultplingo grid sample '--plog' # Default sample mode is timeout
./script/run_bm.sh bm_b10 plingo grid sample '-b10 --plog' # '-b10 's-ould' be transformed to option -b10
./script/run_bm.sh bm_b100 plingo grid sample '-b100 --plog' # the extra arguments can be used to uniquely name the results
./script/run_bm.sh bm_b1000 plingo grid sample '-b1000 --plog'
./script/run_bm.sh bm_b10000 plingo grid sample '-b10000 --plog'
./script/run_bm.sh bm_b100000 plingo grid sample '-b100000 --plog'
./script/run_bm.sh bm_b1000000 plingo grid sample '-b1000000 --plog'
./script/run_bm.sh bm_b10000000 plingo grid sample '-b10000000 --plog'

# Other P-Log benchmarks
./script/run_bm.sh bm plingo nasa exact '--plog' 
./script/run_bm.sh bm plingo squirrel exact '--plog'
./script/run_bm.sh bm plingo blocks exact '--plog'

./script/run_bm.sh bm plog nasa exact
./script/run_bm.sh bm plog squirrel exact
./script/run_bm.sh bm plog blocks exact

./script/run_bm.sh bm plog-dco nasa exact
./script/run_bm.sh bm plog-dco squirrel exact
./script/run_bm.sh bm plog-dco blocks exact

# LPMLN benchmarks
./scripts/run_bm.sh bm plingo alzheimer_problog mpe
./scripts/run_bm.sh bm_default plingo alzheimer_problog mpe '--unsat' # unsat should be transformed to --unsat
./scripts/run_bm.sh bm azreasoners alzheimer_problog mpe

./scripts/run_bm.sh bm plingo smokers mpe
./scripts/run_bm.sh bm_unsat plingo smokers mpe '--unsat'
./scripts/run_bm.sh bm azreasoners smokers mpe
