#./scripts/run_bm.sh plingo birds
#./scripts/run_bm.sh problog birds
#./scripts/run_bm.sh azreasoners birds


# Grid benchmark
# TODO: The corrrect encodings (encoding_problog.lp or encoding_plog.lp) 
# needs to be pasted inside the encoding.lp file before running
./script/run_bm.sh bm_plog plingo grid exact '--plog'
./script/run_bm.sh bm_problog plingo grid exact

./script/run_bm.sh bm plog grid exact
./script/run_bm.sh bm plog-dco grid exact
./script/run_bm.sh bm problog grid exact

./script/run_bm.sh bm grid sample '--plog' # Default sample mode is timeout
./script/run_bm.sh bm_b10 plingo grid sample '-b10 --plog'
./script/run_bm.sh bm_b100 plingo grid sample '-b100 --plog'
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
./scripts/run_bm.sh bm_unsat plingo alzheimer_problog mpe '--unsat'
./scripts/run_bm.sh bm azreasoners alzheimer_problog mpe

./scripts/run_bm.sh bm plingo smokers mpe
./scripts/run_bm.sh bm_unsat plingo smokers mpe '--unsat'
./scripts/run_bm.sh bm azreasoners smokers mpe
