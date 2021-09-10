#script (python)
from clingo import Number, String
from math import log as mathlog

def log(a):
    if a.string == '0':
        pass
        # TODO: Raise Error
    ln = mathlog(float(eval(a.string)))
    weight = Number(int(ln * (10**5))*(-1))
    return weight

def frac(n,d):
    numerator = n.number
    denominator = d.number
    return String(f'{numerator}/{denominator}')

def intprob(a):
    return Number(int(float(eval(a.string))*100))

#end.

% Sort declarations
sort(dice, (d1;d2)).
sort(ball, (b1;b2)).
sort(score, (1;2;3;4;5;6)).
sort(person, (mike;john)).
sort(boolean, (t;f)).

% Attributes
attribute(roll, domain((dice, D)), range(score, Y)) :- sort(dice, D), sort(score, Y).
attribute(owner, domain((dice, D)), range(person, P)) :- sort(dice, D), sort(person, P).
attribute(even, domain((dice, D)), range(boolean, B)) :- sort(dice, D), sort(boolean, B).

attribute(Name, Domain) :- attribute(Name, Domain, Range).
attribute(Name) :- attribute(Name, Domain, Range).

% Regular part
hold(attribute(owner, domain((dice, d1)), range(person, mike))).
hold(attribute(owner, domain((dice, d2)), range(person, john))).
hold(even, domain((dice,D)), range(boolean, t)) :- hold(roll, domain((dice, D)), range(score, Y)), Y \ 2 = 0.
-hold(even, domain((dice, D)), range(boolean, t)) :- not hold(even, domain((dice,D)), range(boolean, t)), sort(dice, D).

% Random selection rules
random(r1, roll, ()).

% Probability atoms
% &pratom(roll(D, Y), "1/6") :- owner(D,john), score(Y).
% &pratom(roll(D, 6), "1/4") :- owner(D, mike).
% &pratom(roll(D, Y), "3/20") :- Y != 6, owner(D, mike).

% TODO: Include variables in sort terms
pratom(r1, attribute(roll, domain((dice,D)), range(score,Y)), "1/6") :- hold(attribute(owner, domain((dice,D)), 
                                                                        range(person, john))), 
                                                                        sort(score, Y), sort(dice, D).
pratom(r1, attribute(roll, domain((dice,D)), range(score,6)), "1/4") :- hold(attribute(owner, domain((dice,D)), range(person, mike))), sort(score, Y), sort(dice, D).
% pratom(r1, attribute(roll, domain((dice,D)), range(score,Y)), "3/20") :- hold(attribute(owner, 
%                                                                         domain((dice,D)), 
%                                                                         range(person, mike))), 
%                                                                         Y != 6, 
%                                                                         sort(score, Y), sort(dice, D).


% Unique value for each attribute
-hold(attribute(Name, Domain, range(R, Y1))) :- hold(attribute(Name, Domain, range(R, Y2))), Y1 != Y2, sort(R, Y1).

% fixed attributes will not be considered random
intervene(attribute(Name, Domain)) :- do(attribute(Name, Domain, Range)).

% Generation rule for random rules
1 {hold(attribute(Name, Domain, range(Sort,Y))) : sort(Sort,Y)}1 :- random(_, Name, _), 
                                                                attribute(Name, Domain, 
                                                                range(Sort,_)), 
                                                                not intervene(attribute(Name, Domain)).

% Observations have to be true in the answer set
:- obs(attribute(Name, Domain, Range)), not hold(attribute(Name,Domain,Range)).
:- obs(-attribute(Name, Domain, Range)), not -hold(attribute(Name,Domain,Range)).

% Actions make literals true
hold(attribute(Name, Domain, Range)):- do(attribute(Name, Domain, Range)).

% Observations and actions
% obs(-attribute(roll, domain((dice,1)), range(score, 1))).
% do(attribute(roll, domain((dice,d1)), range(score,1))).

% Possible atoms
poss(RandomIdentifier, attribute(AttrName, Domain, Range)) :- attribute(AttrName, Domain, Range), 
                                                random(RandomIdentifier, AttrName, SetTerm), 
                                                not intervene(attribute(AttrName, Domain)).

% TODO: Implement dynamic range
% Assigned Probability
posswithassprob(RandomIdentifier, Attr) :- pratom(RandomIdentifier, Attr, Prob), poss(RandomIdentifier, Attr).
assprob(RandomIdentifier, Attr) :- hold(Attr), posswithassprob(RandomIdentifier, Attr).
:~ not assprob(RandomIdentifier, Attr), pratom(RandomIdentifier, Attr, Prob). [@log(Prob)@0]
posswithassprob(Attr) :- posswithassprob(RandomIdentifier, Attr).

% Default probability
posswithdefprob(Attr) :- poss(RandomIdentifier, Attr), not posswithassprob(RandomIdentifier, Attr).
numdefprob(attribute(Name, Domain), X) :- hold(attribute(Name, Domain, range(R, Y1))), 
                                        posswithdefprob(attribute(Name, Domain, range(R, Y1))),
                                        X = #count{Y2 : posswithdefprob(attribute(Name, Domain, range(R,Y2)))}.
cardinality_numdefprob(M) :- numdefprob(_, M).

:~ not numdefprob(attribute(Name, Domain), M), cardinality_numdefprob(M), attribute(Name, Domain). [@log(@frac(1,M))@0]

% Numerator for default probability
remprob(attribute(AttrName, Domain), 100-S) :- random(RandomIdentifier, AttrName, SetTerm), 
                        Attr = attribute(AttrName, Domain, _),
                        hold(Attr), 
                        posswithdefprob(Attr), 
                        S = #sum{@intprob(Prob) : posswithassprob(RandomIdentifier, attribute(Name, Domain, range(R, Y))), pratom(RandomIdentifier, attribute(Name, Domain, range(R, Y)), Prob)}.
totaldefprob(Attr2, X) :- remprob(Attr2, X), X > 0.
:~ not totaldefprob(Attr2, X), remprob(Attr2, X). [@log(@frac(X,100))@0]
:- remprob(Attr2, X), X <= 0.

% Convert meta attributes back to readable output
roll(D, Y) :- hold(attribute(roll, domain((dice, D)), range(score, Y))).
person(D, Y) :- hold(attribute(owner, domain((dice, D)), range(person, Y))).
even(D, Y) :- hold(attribute(even, domain((dice, D)), range(boolean, Y))).

#show remprob/2.