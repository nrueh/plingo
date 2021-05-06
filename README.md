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

In general the conversion will look like the following
```
unsat :- body, not head.
head :- body, not unsat.
:~ unsat.
```

By default, only soft rules are converted to to ASP. To convert hard rules as well, the `--hr` flag can be added on the command line. 

## Examples

### Integrity constraints (bug that has been fixed)
Look at the following program containing an integrity constraint
```
:- a.
a.
```
When the conversion above is implemented directly, the integrity constaint will be converted to
```
unsat(0,"alpha") :- not #false; a.
#false :- not unsat(0,"alpha"); a.
:~ unsat(0,"alpha"). [1@1]
````
However, it appears that the grounder does not evaluate `not #false` to true, but rather that this expression can never be derived to be true. The result is that the grounder removes all of the three rules above and only keeps the integrity constraint. There will be only one stable model `{unsat(1,"alpha")}`, which means the second rule is not satisfied and so atom `a` is never true. In theory there should be an additional stable model, `{a, unsat(0,"alpha")}`, where the integrity constraint is not satisfied and so atom `a` can be true. 
We fix this by explicitly replacing the `not #false`, with `#true` when the rule is an integrity constraint. 
### Simple choice rules (bug that has been fixed)
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
UPDATE: This was a bug that has been fixed. Now `not {a}` is always false, so that the `unsat` atom is never true and we end up with the only the choice rule `{a}.` again after the conversion.

### Aggregates with pooling
Next consider the rule
```
{a; b; c} = 2. 
```
Here exactly two of the atoms should be chosen. Other than a simple choice rule, this cannot be naturally expressed within LPMLN. With the ``--hr`` flag, we get the following conversion
```
unsat(0,"alpha") :- not 2 = { a; b; c }.
2 = { a; b; c } :- not unsat(0,"alpha").
:~ unsat(0,"alpha"). [1@1]
```
The grounder replaces the aggregates with two `#delayed` statements and in this case we can enumerate all stable models which are `{a,b}`, `{a,c}`, `{b,c}` and `{unsat(0,"alpha)}`. In the last stable model the rule is not satisfied so we do not get any other atoms. 

### Intervals and pooling
Next we consider intervals and pooling in general. Take the following program
```
size(2).
grid(1..S,1..S) :- size(S).
```
The conversion looks as follows
```
unsat(0,"alpha") :- not size(2).
size(2) :- not unsat(0,"alpha").
:~ unsat(0,"alpha"). [1@1]

unsat(1,"alpha",S) :- not grid((1..S),(1..S)); size(S).
grid((1..S),(1..S)) :- not unsat(1,"alpha",S); size(S).
:~ unsat(1,"alpha",S). [1@1]
```
Although the second rule instantiates four `grid/2` atoms, it only has one unsat atom. That means that either the entire rule is unsatisfied and no `grid/2` atoms are true, or all of them are true (in case the first rule is satisfied as well). Would it be desirable here to be able to (de)activate only some of the `grid/2` atoms? 
Such thing would be possible if we pass along the interval information to the unsat atom in which case multiple unsat atoms will be instantiated. A naive approach would be to add the interval to the unsat atom
```
unsat(1, "alpha", S, (1..S),(1..S)) :- not grid((1..S),(1..S)); size(S).
```
However, this instantiates too many unsat atoms. Instead we would like the interval values to match. This can be achieved by binding the intervals to a variable and replacing the intervals inside the atoms with that variable.
```
unsat(1, "alpha", S, Int1, Int2) :- not grid(Int1, Int2,); size(S), Int1=(1..S), Int2=(1..S).
```
Here variables `Int1` and `Int2` are placeholders for the intervals. With this replacement we would get many stable models where all, none or some of the `grid/2` atoms are true.

### Intervals and pooling with aggregates again
Binding intervals (or pooling) to variables can also lead to clearly undesired behavior. Consider the following example that combines intervals with aggregates.
```
{m(1..3) } = 1.
```
Here the desired behavior is have exactly one `m/1` atom. However, if we bind the interval to a variable as described above we instantiate three aggregates rules. And so it will be possible to have more than `m/1` atom to be true. 

### Correct model cost
Program with only choice rules, does not have any model costs. How to handle that case?
```
{a}.
```

Program with only hard rules, has only model costs at level 1. How to check that, pass that information to probability module?
```
b.
```
Vice versa program with only soft rules and option '--hr' has only model costs at level 0.
```
b :- &weight(1).
```