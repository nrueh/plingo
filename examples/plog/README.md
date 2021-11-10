# P-log examples
This directory contains the five examples from [[1]](#1) plus a variant of the Monty Hall problem taken from [[2]](#2). To run any of the examples add the `--plog` option.

## Instances
### Dice
This is the introductory example from [[1]](#1) demonstrating how P-log programs can be input and calculated with our system. 
```
python lpmln.py examples/plog/dice.lp --plog --all
```

### Monty Hall
P-log encoding of the famous Monty Hall Problem
```
python lpmln.py examples/plog/monty_hall.lp --plog --all
```
There is also a variation with four door and assigned probabilities
```
python lpmln.py examples/plog/monty_hall_variant.lp --plog --all
```

### Simpson's paradox
Simpson's paradox is a phenomenom where some event seems more likely in the general population but less likely in every subpopulation (or vice versa). In this case we are looking at a patient wondering whether he should take a drug or not. For both females and males not taking the drug has a higher recovery rate. However, when looking at the entire population the recovery rate is actually lower when taking the drug. One way to resolve this paradox is by using the causal reasoning of P-log. For adjusting whether or not the patient takes the drug, set constant `do_drug` to `t` or `f` (default is `do_drug=t`). 
```
python lpmln.py examples/plog/simpsons_paradox.lp --plog --all -c do_drug=t
```


## References
<a id="1">[1]</a>
M. Gelfond C. Baral and J.N. Rushton (2009).
Probabilistic reasoning with answer sets.
Theory and Practice of Logic Programming, 9(1),57–144.

<a id="2">[2]</a>
J. Lee, Z. Yang (2017).
LPMLN, Weak Constraints and P-log.
Proceedings of the 31st AAAI Conference on Artificial Intelligence, 1170–1177.
