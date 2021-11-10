# P-log examples
This directory contains the five examples from [[1]](#1) plus a variant of the Monty Hall problem taken from [[2]](#2). To run any of the examples add the `--plog` option. The file `meta.lp` is used by our system. Since in that file all meta atoms have `_lpmln` prepended, there is an additional `meta_readable.lp` which contains the same rules without the prefix.

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
Simpson's paradox is a phenomenom where some event seems more likely in the general population but less likely in every subpopulation (or vice versa). In this case we are looking at a patient who is wondering whether he should take a drug or not. For both females and males not taking the drug has a higher recovery rate. However, when looking at the entire population the recovery rate seems to be lower when taking the drug. One way to resolve this paradox is by using the causal reasoning of P-log. For adjusting whether or not the patient takes the drug, set constant `do_drug` to `t` or `f` (default is `do_drug=t`). 
```
python lpmln.py examples/plog/simpsons_paradox.lp --plog --all -c do_drug=t
```

### Moving robot
This encoding contains a robot and three doors that are reachable from the robot's position. The doors can be open or closed but the robot cannot open the doors. It is known that the robot navigation is usually successful. However, a malfunction can cause the robot to go off course and enter any one of the open rooms. The basic encoding contains some additional information that can be activated through the constant `x`. While `x=0` contains only the basic encoding, when `x=1`  there is an additional fact that the robot goes into room `r0`.
```
python lpmln.py examples/plog/moving_robot.lp --plog --all -c x=1
```
Accordingly, the output states that the robot is in room `r0`.
```
Solving...
Answer: 1
in(1,r0)
No soft weights in program. Cannot calculate probabilites
SATISFIABLE
```
For `x=2` the robot is now addtionally malfunctioning which activates the random selection rule. 
```
python lpmln.py examples/plog/moving_robot.lp --plog --all -c x=2
```
Now it is uncertain in what room the robot will land and there are three possible worlds with equal probability. 
```
Solving...
Answer: 1
in(1,r0)
Optimization: 109861
Answer: 2
in(1,r1)
Optimization: 109861
Answer: 3
in(1,r2)
Optimization: 109861


Probability of Answer 1: 0.33333
Probability of Answer 2: 0.33333
Probability of Answer 3: 0.33333
```
Finally, `x=3` adds more probability information.


### Bayesian squirrel
## References
<a id="1">[1]</a>
M. Gelfond C. Baral and J.N. Rushton (2009).
Probabilistic reasoning with answer sets.
Theory and Practice of Logic Programming, 9(1),57–144.

<a id="2">[2]</a>
J. Lee, Z. Yang (2017).
LPMLN, Weak Constraints and P-log.
Proceedings of the 31st AAAI Conference on Artificial Intelligence, 1170–1177.
