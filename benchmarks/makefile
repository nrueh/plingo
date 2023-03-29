SHELL=/bin/bash

copy-programs:
	cp -r programs/* systems/benchmark-tool/programs
	cp -r programs/runsolver-3.4.0 systems/benchmark-tool
	cp programs/clingo.py systems/benchmark-tool/src/benchmarktool/resultparser
clean-results:
	rm -rf ./results/*
clean-output:
	rm -rf systems/benchmark-tool/output/*
clean-runscripts:
	rm -rf ./runscripts/runscript_*_*_*_*_*
clean:
	rm -rf fault_runsolver.txt
	make clean-runscripts
	make clean-output
$(eval PATH_BASE = dom/$(DOM)/$(APP))

mpe:
ifeq ($(APP), plingo)
	plingo $(INS) $(PATH_BASE)/encoding.lp -q2 $(EXTRA)
endif
ifeq ($(APP), plingo-problog)
	plingo $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp -q2 $(EXTRA) --problog=$(INS)_problog.lp >/dev/null ; problog mpe $(INS)_problog.lp 
endif
ifeq ($(APP), problog)
	problog mpe $(INS) -v $(EXTRA)
	exit 0
endif
ifeq ($(APP), azreasoners)
	python systems/azreasoners/lpmln_infer.py show.lp $(INS) $(PATH_BASE)/encoding.lp $(EXTRA) | sed '/Answer:/,+2 d'
endif

exact:
ifeq ($(APP), plingo)
	plingo $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp -q2 $(EXTRA)
endif
ifeq ($(APP), plingo-problog)
	plingo $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp -q2 $(EXTRA) --problog=$(INS)_problog.lp >/dev/null ; problog $(INS)_problog.lp ; rm $(INS)_problog.lp
endif
ifeq ($(APP), problog)
	problog $(INS)
	exit 0
endif
ifeq ($(APP), azreasoners)
	python systems/azreasoners/lpmln_infer.py show.lp $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp -exact -q query $(EXTRA) | sed '/Answer:/,+2 d'
endif
ifeq ($(APP), plog)
	./systems/plog/plog2 $(INS) $(EXTRA)
endif

sample:
# ifeq ($(APP), plingo)
# 	plingo $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp --opt-enum -q2 -b$(N) $(EXTRA)
# endif
ifeq ($(APP), plingo)
	plingo $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp --opt-enum -q2 $(EXTRA)
endif
# ifeq ($(APP), problog)
# 	problog sample $(INS) --estimate -N $(N) $(EXTRA)
# 	exit 0
# endif
# ifeq ($(APP), azreasoners)
# 	source /usr/local/apps/anaconda3/etc/profile.d/conda.sh && conda activate lpmln && python systems/azreasoners/lpmln_infer.py show.lp $(INS) $(PATH_BASE)/encoding.lp $(PATH_BASE)/query.lp  -mcasp -samp $(N) -q query && conda activate plingo $(EXTRA)
# endif


