#script (python)
from clingo import Number, String
from math import log as mathlog

def log(a, factor):
    factor = factor.number
    if a.string == '0':
        pass
        # TODO: Raise Error
    ln = mathlog(float(eval(a.string)))
    weight = Number(int(ln * (10**factor)))
    return weight

def frac(n,d):
    return String(f'{n.number}/{d.number}')

def intprob(a):
    factor = 10**6
    if str(a.type) == 'SymbolType.String':
        return Number(int(float(eval(a.string))*factor))
    elif str(a.type) == 'SymbolType.Number':
        return Number(a.number*factor)
#end.

% Create boolean sort
sort(boolean, t).
sort(boolean, f).

% Create attribute atoms without range
attribute(Name, Domain) :- attribute(Name, Domain, Range).

% Unique value for each attribute
-hold(attribute(Name, Domain, sort(R, Y1))) :- hold(attribute(Name, Domain, sort(R, Y2))), Y1 != Y2, sort(R, Y1).

% fixed attributes will not be considered random
intervene(attribute(Name, Domain)) :- do(hold(attribute(Name, Domain, Range))).
intervene(attribute(Name, Domain)) :- do(-hold(attribute(Name, Domain, Range))).

% Generation rule for random selection rules without set term
1 {hold(attribute(Name, Domain, sort(Sort,Y))) : sort(Sort,Y)}1 :- random(_, Name), 
                                                                attribute(Name, Domain, sort(Sort,_)), 
                                                                not intervene(attribute(Name, Domain)).

% Generation rule for random selection rules with set term
1 {hold(attribute(Name, Domain, sort(Sort,Y))) : sort(Sort,Y), hold(SetTerm, sort(Sort, Y))}1 :- random(_, Name, SetTerm), 
                                                                attribute(Name, Domain, sort(Sort,_)), 
                                                                not intervene(attribute(Name, Domain)).

% Observations have to be true in the answer set
:- obs(hold(attribute(Name, Domain, Range))), not hold(attribute(Name,Domain,Range)).
:- obs(-hold(attribute(Name, Domain, Range))), not -hold(attribute(Name,Domain,Range)).

% Actions make literals true
hold(attribute(Name, Domain, Range)):- do(hold(attribute(Name, Domain, Range))).
-hold(attribute(Name, Domain, Range)):- do(-hold(attribute(Name, Domain, Range))).

% Possible atoms for random selection rules without set term
poss(RandomIdentifier, attribute(AttrName, Domain, Range)) :- attribute(AttrName, Domain, Range), 
                                                random(RandomIdentifier, AttrName),
                                                not intervene(attribute(AttrName, Domain)).

% Possible atoms for random selection rules with set term
poss(RandomIdentifier, attribute(AttrName, Domain, Range)) :- attribute(AttrName, Domain, Range), 
                                                random(RandomIdentifier, AttrName, SetTerm), hold(SetTerm, Range),
                                                not intervene(attribute(AttrName, Domain)).

% Assigned Probability
posswithassprob(RandomIdentifier, Attr) :- pratom(RandomIdentifier, Attr, Prob), poss(RandomIdentifier, Attr).
assprob(RandomIdentifier, Attr) :- hold(Attr), posswithassprob(RandomIdentifier, Attr).
:~ not assprob(RandomIdentifier, Attr), pratom(RandomIdentifier, Attr, Prob). [@log(Prob, factor)@0,assigned,RandomIdentifier,Attr]
posswithassprob(Attr) :- posswithassprob(RandomIdentifier, Attr).

% Default probability
posswithdefprob(Attr) :- poss(RandomIdentifier, Attr), not posswithassprob(RandomIdentifier, Attr).
numdefprob(attribute(Name, Domain), X) :- hold(attribute(Name, Domain, sort(R, Y1))), 
                                        posswithdefprob(attribute(Name, Domain, sort(R, Y1))),
                                        X = #count{Y2 : posswithdefprob(attribute(Name, Domain, sort(R,Y2)))}.

% Helper atom for numdefprob weak constraint
range_cardinality(Name, X) :- attribute(Name, Domain), X = #count{Y : attribute(Name, Domain, sort(R,Y))}.

:~ not numdefprob(attribute(Name, Domain), M), posswithdefprob(attribute(Name, Domain, _)), range_cardinality(Name, X), M=2..X. [@log(@frac(1,M), factor)@0,denominator,Name,Domain]

% Numerator for default probability
percentage(@intprob(1)-S, Domain) :- 
                    attribute(_, Domain), 
                    S = #sum{@intprob(Prob), Y : posswithassprob(RandomIdentifier, attribute(Name, Domain, sort(R, Y))), pratom(RandomIdentifier, attribute(Name, Domain, sort(R, Y)), Prob)}.

remprob(attribute(AttrName, Domain), X) :- 
                        Attr = attribute(AttrName, Domain, _),
                        hold(Attr), 
                        posswithdefprob(Attr), 
                        percentage(X, Domain).


% remprob(attribute(AttrName, Domain), 100-S) :- random(RandomIdentifier, AttrName, SetTerm), 
%                         Attr = attribute(AttrName, Domain, _),
%                         hold(Attr), 
%                         posswithdefprob(Attr), 
%                         S = #sum{@intprob(Prob) : posswithassprob(RandomIdentifier, attribute(Name, Domain, sort(R, Y))), pratom(RandomIdentifier, attribute(Name, Domain, sort(R, Y)), Prob)}.



totaldefprob(Attr, X) :- remprob(Attr, X), X > 0.

% Helper atom for weak constraint generation
percentage(X) :- percentage(X, _).
:~ not totaldefprob(attribute(Name, Domain), X), posswithdefprob(attribute(Name, Domain,_)), percentage(X). [@log(@frac(X,@intprob(1)), factor)@0,numerator,Name, Domain]

% Percentages cannot be negative
:- remprob(Attr, X), X <= 0.