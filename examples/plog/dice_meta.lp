#include "../../plog_meta.lp".

% Sort declarations
sort(dice, (d1;d2)).
sort(score, (1;2;3;4;5;6)).
sort(person, (mike;john)).
% sort(boolean, (t;f)).

dice(D) :- sort(dice, D).
score(Y) :- sort(score, Y).
person(P) :- sort(person, P).

% Attributes
attribute(roll, domain(sort(dice, D)), sort(score, Y)) :- sort(dice, D), sort(score, Y).
attribute(owner, domain(sort(dice, D)), sort(person, P)) :- sort(dice, D), sort(person, P).
attribute(even, domain(sort(dice, D)), ()) :- sort(dice, D).

% Regular part
owner(d1, mike).
owner(d2, john).
even(D) :- roll(D,Y), Y \ 2 = 0.
-even(D) :- not even(D), dice(D).

% Random selection rules
random(r1, roll).

% Probability atoms
pratom(r1, attribute(roll, domain(sort(dice,D)), sort(score, Y)), "1/6") :- hold(attribute(owner, domain(sort(dice,D)), sort(person, john))), 
                                                                        sort(score, Y).
pratom(r1, attribute(roll, domain(sort(dice,D)), sort(score,6)), "1/4") :- hold(attribute(owner, domain(sort(dice,D)), sort(person, mike))).
pratom(r1, attribute(roll, domain(sort(dice,D)), sort(score,Y)), "3/20") :- hold(attribute(owner, 
                                                                        domain(sort(dice,D)), 
                                                                        sort(person, mike))), 
                                                                        Y != 6, 
                                                                        sort(score, Y), sort(dice, D).


% Observations and actions
obs(hold(attribute(roll, domain(sort(dice, d2)), sort(score, 1)))).
% do(hold(attribute(roll, domain(sort(dice,d1)), sort(score,1)))).


% Convert meta attributes back to readable output
roll(D, Y) :- hold(attribute(roll, domain(sort(dice, D)), sort(score, Y))).
owner(D, Y) :- hold(attribute(owner, domain(sort(dice, D)), sort(person, Y))).
even(D) :- hold(attribute(even, domain(sort(dice, D)), ())).

hold(attribute(roll, domain(sort(dice, D)), sort(score, Y))) :- roll(D,Y).
hold(attribute(owner, domain(sort(dice, D)), sort(person, Y))) :- owner(D,Y).
hold(attribute(even, domain(sort(dice, D)), ())) :- even(D).
#show roll/2.