# Relaxed clique

This directory contains everything related to the Relaxed Clique benchmark which has been taken from  [[1]](#1) and used for comparison to their system. The encoding can be found in `relaxed_clique.lp`. The directory `az_instances` contains the original instances used in that paper together with a file `gen.py` which has been used for generation of the instances. In the folder `runtimes` the two files starting with `runtime_az_instance_SYSTEM.csv` contain the runtimes on these instances with our system and a newer version of the system from [[1]](#1). We visualized the results from both files in two graphs (`figures/relaxed_clique_az_instances_SYSTEM.png`).

Run an instance from the root of this repository with e.g.
```
python plingo.py benchmarks/relaxed_clique/relaxed_clique.lp benchmarks/relaxed_clique/az_instances/p50n10
```
In the thesis we limited the computation to 20 minutes (using the option `--time-limit 1200`).


## References
<a id="1">[1]</a>
J. Lee, S. Talsania, and Y. Wang (2017).
Computing LPMLN Using ASP and MLN Solvers.
Journal of Theory and Practice of Logic Programming, 17(5-6), 942-960.
