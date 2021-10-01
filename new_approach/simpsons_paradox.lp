% Sort declarations
boolean(t;f).

% Regular part

% Random selection rules
_random(r1, (male, (), B)) :- boolean(B).
_random(r2, (recover, (), B)) :- boolean(B).
_random(r3, (drug, (), B)) :- boolean(B).

% Probability atoms
_pr(r1, (male, (), t), "1/2").
_pr(r2, (recover, (), t), "0.6") :- male(t), drug(t).
_pr(r2, (recover, (), t), "0.7") :- male(t), drug(f).
_pr(r2, (recover, (), t), "0.2") :- male(f), drug(t).
_pr(r2, (recover, (), t), "0.3") :- male(f), drug(f).
_pr(r3, (drug, (), t), "0.75") :- male(t).
_pr(r3, (drug, (), t), "0.25") :- male(f).


%
% Additional
%
_h((male, (), B)) :- male(B).
male(B) :- _h((male, (), B)).

_h((recover, (), B)) :- recover(B).
recover(B) :- _h((recover, (), B)).

_h((drug, (), B)) :- drug(B).
drug(B) :- _h((drug, (), B)).

% Observations and actions
_do((drug, (), f)).

#show male/1.
#show recover/1.
#show drug/1.

#show pratom/3.
#show assprob/2.