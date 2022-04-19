# Benchmarks

This directory contains a number of different domains to benchmark:
- Relaxed Clique from [[1]](#1)
- Link prediction
- Birds (Small example for testing)

## Additional systems

Other systems are installed as submodules and require installations

#### Update submodules

```
git submodule update --recursive --remote --init
```

**ProbLog**

```shell
cd systems/problog
pip install .
```

**Azreasoners**

```shell
cd systems/azreasoners
python setup.py
```

**Plog**

```shell
cd systems/plog
git submodule update --recursive --remote --init
cmake .
make
```

## Benchamrks 

For a given domain `$DOM` such as `link-prediction` for every instance `$INS`

#### MAP estimate
- **plingo**: `plingo $INS $ENCODING`
  Clingo stats Solving time
- **problog**: `problog mpe $INS`
  [INFO] Solving: 0.0273s
- **lpmln**: `python lpmln-infer.py $INS $ENCODING --verbosity 1`
  Clingo stats Solving time


#### Marginal probability (exact)
- **plingo**: `plingo --all $INS $ENCODING `
```
query.lp -q 2
plingo version 1.0
Reading from dom/birds/plingo/instances/birds.lp ...
Solving...


query: 0.66524


OPTIMUM FOUND

Models       : 3
  Optimum    : yes
Calls        : 1
Time         : 0.005s (So
```
- **problog**: `problog $INS`
```
[INFO] Output level: INFO
[INFO] Propagating evidence: 0.0000s
[INFO] Grounding: 0.0010s
[INFO] Cycle breaking: 0.0001s
[INFO] Clark's completion: 0.0000s
[INFO] DSharp compilation: 0.0065s
[INFO] Total time: 0.0123s
query:	0.67
(True, {query: 0.67})
```

- **lpmln**: `python lpmln-infer.py $INS $ENCODING -all -exact` 
```
opt-mode=enum: No bound given, optimize statement ignored.

query : 0.6652409557748219
```


#### Sample (approximate)

Given a sample size `$N`

- **plingo**: `plingo $INS $ENCODING $QUERY --opt-enum -q1 -b{$N/2}`
```
plingo version 1.0
Reading from dom/birds/plingo/instances/birds.lp ...
Solving...
Solving...
Solving...
Solving...


query: 0.66524


UNSATISFIABLE

Models       : 8
Calls        : 4
Time         : 0.006s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.015s
```
- **problog**: `problog sample $INS --estimate -N $N`

```
% Probability estimate after 10 samples (1068.3675 samples/second):
query:  0.5 
```

- **lpmln**: `python lpmln-infer.py $INS $ENCODING $QUERY -mcasp -samp $N -q query`

## What results do we need?

- Global Time?
- Clingo Times?
- Probability?


## References
<a id="1">[1]</a>
J. Lee, S. Talsania, and Y. Wang (2017).
Computing LPMLN Using ASP and MLN Solvers.
Journal of Theory and Practice of Logic Programming, 17(5-6), 942-960.
