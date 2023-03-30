
# Grid benchmark
# TODO: The corrrect encodings (encoding_problog.lp or encoding_plog.lp)
# needs to be pasted inside the encoding.lp file before running
#cat ./dom/grid/plingo/encoding_problog.lp > ./dom/grid/plingo/encoding.lp
#./scripts/run_bm.sh bm plingo-problog grid exact '--frontend=problog'

# Other P-Log benchmarks
./scripts/run_bm.sh bm plingo-problog nasa exact '--frontend=plog'
./scripts/run_bm.sh bm plingo-problog squirrel exact '--frontend=plog'
./scripts/run_bm.sh bm plingo-problog blocks exact '--frontend=plog'

# LPMLN benchmarks
./scripts/run_bm.sh bm plingo-problog alzheimer_problog mpe '--frontend=lpmln-alt'

./scripts/run_bm.sh bm plingo-problog smokers mpe '--frontend=lpmln-alt'

