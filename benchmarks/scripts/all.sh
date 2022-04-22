#./scripts/run_bm.sh plingo birds
#./scripts/run_bm.sh problog birds
#./scripts/run_bm.sh azreasoners birds


# Grid benchmark
# TODO: The corrrect encodings (encoding_problog.lp or encoding_plog.lp) 
# needs to be pasted inside the encoding.lp file before running
./scripts/run_bm.sh bm_plog plingo grid exact '--plog'
./scripts/run_bm.sh bm_problog plingo grid exact

./scripts/run_bm.sh bm plog grid exact
./scripts/run_bm.sh bm plog-dco grid exact
./scripts/run_bm.sh bm problog grid exact

./scripts/run_bm.sh bm grid sample '--plog' # Default sample mode is timeout
./scripts/run_bm.sh bm_b10 plingo grid sample '-b10 --plog'
./scripts/run_bm.sh bm_b100 plingo grid sample '-b100 --plog'
./scripts/run_bm.sh bm_b1000 plingo grid sample '-b1000 --plog'
./scripts/run_bm.sh bm_b10000 plingo grid sample '-b10000 --plog'
./scripts/run_bm.sh bm_b100000 plingo grid sample '-b100000 --plog'
./scripts/run_bm.sh bm_b1000000 plingo grid sample '-b1000000 --plog'
./scripts/run_bm.sh bm_b10000000 plingo grid sample '-b10000000 --plog'

# Other P-Log benchmarks
./scripts/run_bm.sh bm plingo nasa exact '--plog' 
./scripts/run_bm.sh bm plingo squirrel exact '--plog'
./scripts/run_bm.sh bm plingo blocks exact '--plog'

./scripts/run_bm.sh bm plog nasa exact
./scripts/run_bm.sh bm plog squirrel exact
./scripts/run_bm.sh bm plog blocks exact

./scripts/run_bm.sh bm plog-dco nasa exact
./scripts/run_bm.sh bm plog-dco squirrel exact
./scripts/run_bm.sh bm plog-dco blocks exact

# LPMLN benchmarks
./scripts/run_bm.sh bm plingo alzheimer_problog mpe
./scripts/run_bm.sh bm_unsat plingo alzheimer_problog mpe '--unsat'
./scripts/run_bm.sh bm azreasoners alzheimer_problog mpe

./scripts/run_bm.sh bm plingo smokers mpe
./scripts/run_bm.sh bm_unsat plingo smokers mpe '--unsat'
./scripts/run_bm.sh bm azreasoners smokers mpe
