# LPMLN
An implementation to compute LPMLN programs using clingo.

## Introduction
LPMLN is a probabilistic logic language that provides a simple way to add weights to ASP-style rules. This not only make it possible to reason with uncertainty but also to resolve inconsistencies in the rules. In that way meaningful information can be extracted from a program even if there are two or more contradicting rules.
Further the Maximum a posteriori (MAP) estimate, the most probable stable model, can be inferred from a program using LPMLN.


## Installation
The program depends on Python 3 and clingo 5.5. Its easiest to install with Anaconda 
```
conda install -c potassco/label/dev clingo
```
See https://potassco.org/clingo/ for further information.


## Usage
To try out the program just run the file `lpmln.py` in python with any LPMLN instance appended. For example
```
python lpmln.py birds.lp
```
This gives the MAP estimate. To list all stable models, add the flag `--all`. 
```
python lpmln.py birds.lp --all
```
## Input
Syntactically, in LPMLN we differ between "soft" rules and "hard" rules, where "soft" rules have an integer weight and "hard" rules the weight "alpha". 

Weights can be added by using the theory atom `&weight/1`, so e.g. `&weight(5)`, to the body of a rule. Rules that do not have any weight in the body are assumed to be hard rules by default.

To compute LPMLN programs, a rule in an LPMLN program is converted to three rules in ASP with weak constraints.
Take for example the rule

```
a(X) :- b(X), &weight(5).
```
This gets converted to the following three rules
```
unsat(idx, 5, X) :- b(X), not a(X).
a(X) :- b(X), not unsat(idx, 5, X).
:~ unsat(idx, 5, X). [5@0]
```
where `idx` is the index of the rule in the LPMLN program and the `unsat` atom is True if the original rule is not satisfied. In that case the weak constraint adds the weight of the rule as a penalty. Note that the `unsat` atom contains information about the index, the weight and all variables in a rule.

By default, only soft rules are converted to to ASP. To convert hard rules as well, the `--hr` flag can be added on the command line. 

## Examples

### Integrity constraints
### Simple choice rules
Take the program consisting of the choice rule 
```
{a}.
```
If you use the `--hr` flag, this hard rule will be converted as well. The conversion is
```
unsat(0, "alpha") :- not {a}.
{a} :- not unsat(0,"alpha").
:~ unsat(0,"alpha")
```
Since the body of the first rule `not {a}` is always true, the grounder removes it and `unsat(0, "alpha")` becomes a fact. Thus rendering the second and third rule unnecessary. The only stable model is therefore `unsat(0, "alpha")`, which means the rule `{a}.`is never satisfied and therefore atom `a` never contained in a stable model. This is not the desired behavior. However, since in LPMLN it is already not mandatory for rules to be satisfied, the question is whether choice rules should ever be converted as described above.

### Aggregates with pooling
Next consider the rule
```
{a; b; c} = 2. 
```
Here exactly two of the atoms should be chosen. With the ``--hr`` flag, we get the following conversion
```
unsat(0,"alpha") :- not 2 = { a; b; c }.
2 = { a; b; c } :- not unsat(0,"alpha").
:~ unsat(0,"alpha"). [1@1]
```
The grounder replaces the aggregates with two `#delayed` statements and in this case we can enumerate all stable models which are `{a,b}`, `{a,c}`, `{b,c}` and `{unsat(0,"alpha)}`. In the last stable model the rule is not satisfied so we do not get any other atoms. 
