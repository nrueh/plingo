# clingo-lpmln
A probabilistic extension for clingo based on LP^MLN.

## Introduction
LPMLN is a probabilistic logic language that provides a simple way to add weights to ASP-style rules. This not only make it possible to reason with uncertainty but also to resolve inconsistencies in the rules. In that way meaningful information can be extracted from a program even if there are two or more contradicting rules.
Further the Maximum a posteriori (MAP) estimate, the most probable stable model, can be inferred from a program using LPMLN.


## Installation
The program depends on Python 3, clingo 5.5 and numpy. The requirements are easiest to install with Anaconda 
```
conda install -c potassco/label/dev clingo
conda instal numpy
```
See https://potassco.org/clingo/ for further information.

For installation just clone the repository
```
git clone https://github.com/nrueh/LPMLN.git
```

## Usage
To try out the program run the file `lpmln.py` in python with any LPMLN instance appended. For example
```
python lpmln.py examples/birds.lp
```
This gives the MAP estimate. 
```
clingo-lpmln version 1.0
Reading from examples/birds.lp
Solving...
Answer: 1

Optimization: 300000
Answer: 2
residentBird(jo) bird(jo)
Optimization: 100000
OPTIMUM FOUND

Models       : 2
  Optimum    : yes
Optimization : 100000
Calls        : 1
Time         : 0.005s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.005s
```
To list all stable models, add the flag `--all`. 
```
python lpmln.py birds.lp --all
```
with output 
```
clingo-lpmln version 1.0
Reading from examples/birds.lp
Solving...
Answer: 1

Optimization: 300000
Answer: 2
residentBird(jo) bird(jo)
Optimization: 100000
Answer: 3
migratoryBird(jo) bird(jo)
Optimization: 200000


Probability of Answer 1: 0.09003
Probability of Answer 2: 0.66524
Probability of Answer 3: 0.24473


OPTIMUM FOUND

Models       : 3
  Optimum    : yes
Calls        : 1
Time         : 0.006s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.006s
```
## Input
Syntactically, LPMLN differs between "soft" rules and "hard" rules, where "soft" rules have a (real number) weight and "hard" rules the weight "alpha". 

Weights can be added by the theory atom `&weight/1` to the body of a rule. The argument has to be an integer or a string containing a float or an expression like `2/3`. For example
```
a(X) :- b(X), &weight(5).
b(X) :- &weight("-2/3").
```
Further it is possible to use the theory atoms `&log/1` or `&problog/1` which only accept strings as arguments. The atom `&log/1` uses the natural logarithm `log(p)` of its argument `p` as weight. The atom `&problog/1` uses the natural logarithm of `p/(1-p)` as its weight.
Rules that do not have any weight in the body are assumed to be hard rules.

To compute LPMLN programs, a rule in an LPMLN program is converted to ASP with weak constraints

By default, only soft rules are converted. To convert hard rules as well, the `--hr` flag can be added on the command line. This option essentially makes hard rules optional, whereas in the default setting all hard rules have to be satisfied as usually in ASP.

## Examples
A number of examples can be found in the directory `examples`. There are also two sub-directories containing examples from the other probabilistic logic languages ProbLog and P-log.

## Commandline options
- `--all`

    Enumerates all stable models and prints their probabilities.

- `--evid=file`

    Provides an evidence file to the program (`.lp` file with clingo syntax rules)

- `--hr`

    Converts hard rules as well. Useful for debugging or resolving inconsistencies in the program.

- `--plog`

    Necessary when calculating P-log programs.

- `--q=atom`

    Adds a query atom `atom`. The argument has to be either just the name of the atom (`--q=isPerson`) or the name plus arguments separated by comma (`--q=isPerson,John,Doe` queries for atom `isPerson(John,Doe)`).

- `--two-solve-calls`

    Uses two solve calls: The first one finds the minimal bound for weak constraints priorities higher than 0. The second one solves for probabilistic stable models of LP^MLN.

- `--unsat`

    Uses the conversion with `unsat` atoms
