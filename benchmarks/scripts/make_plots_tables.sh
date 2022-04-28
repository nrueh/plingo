#! /bin/bash

TABLE='-t table --csv'

# Grid
python scripts/plot.py --dom grid --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' -a plingo.bm_plog -a problog.bm -a plog.bm -a plog.bm_dco
python scripts/plot.py --dom grid --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' -a plingo.bm_plog -a plingo.bm_problog
python scripts/plot.py --dom grid --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' -a plingo.bm_plog -a problog.bm -a plog.bm -a plog.bm_dco $TABLE

# Grid approximate
python scripts/plot.py --dom grid --opt sample --prefix 'prob' -a plingo.bm_b10 -a plingo.bm_b100 -a plingo.bm_b1000 -a plingo.bm_b10000 -a plingo.bm_b100000 -a plingo.bm_b1000000 -a problog.bm -t prob

# Nasa
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' --dom nasa -a plog.bm -a plog.bm_dco -a plingo.bm
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' --dom nasa -a plog.bm -a plog.bm_dco -a plingo.bm $TABLE

# Blocks
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' --dom blocks -a plog.bm -a plog.bm_dco -a plingo.bm -t line
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' --dom blocks -a plog.bm -a plog.bm_dco -a plingo.bm
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '' --prefix 'runtime' --dom blocks -a plog.bm -a plog.bm_dco -a plingo.bm $TABLE

# Squirrel
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '#Days' --prefix 'runtime' --dom squirrel -a plog.bm -a plog.bm_dco -a plingo.bm -t line
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '#Days' --prefix 'runtime-log' --dom squirrel -a plog.bm -a plog.bm_dco -a plingo.bm -t line
python scripts/plot.py --opt exact --y 'Runtime (s)' --x '#Days' --prefix 'runtime' --dom squirrel -a plog.bm -a plog.bm_dco -a plingo.bm $TABLE

# Alzheimer
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '' --prefix 'runtime' --dom alzheimer_problog -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm -t line
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '' --prefix 'runtime-log' --dom alzheimer_problog -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm -t line
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '' --prefix 'runtime' --dom alzheimer_problog -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm $TABLE

# Smokers
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '#Person' --prefix 'runtime' --dom smokers -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm -t line 
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '#Person' --prefix 'runtime-log' --dom smokers -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm -t line
python scripts/plot.py --opt mpe --y 'Runtime (s)' --x '#Person' --prefix 'runtime' --dom smokers -a plingo.bm -a plingo.bm_unsat -a azreasoners.bm $TABLE
