# Examples

This directory contains a number of examples taken from LP^MLN, ProbLog and P-log demonstrating the features of our system.


## Instances

### Birds
This example is taken from [[1]](#1) and has been demonstrated. To get all stable models and their probabilities
```
python lpmln.py examples/birds.lp --all
```
or provide evidence
```
python lpmln.py examples/birds.lp --evid=examples/birds_evid.lp --all
```

### Firing Squad
This example is originally from Pearl's causal model  [[2]](#2) and shows counterfactual reasoning. The LP^MLN encoding stems from [[3]](#3). Run it with
```
python lpmln.py examples/firing_squad.lp --evid=examples/firing_squad_evid.lp --q ds
```

## References
<a id="1">[1]</a>
J. Lee and Y. Wang (2016).
Weighted Rules under the Stable Model Semantics.
Proceedings of the 15th International Conference on Principles of Knowledge Representation and Reasoning, 145-154.

<a id="2">[2]</a>
J. Pearl (2000).
Causality: Models, Reasoning and Inference.
Volume 29.

<a id="3">[3]</a>
J. Lee, S. Talsania, and Y. Wang (2017).
Computing LPMLN Using ASP and MLN Solvers.
Journal of Theory and Practice of Logic Programming, 17(5-6), 942-960.
