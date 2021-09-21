% Sort declarations

% Attributes
&attribute(male, (), boolean).
&attribute(recover, (), boolean).
&attribute(drug, (), boolean).

% Regular part

% Random selection rules
random(r1, male).
random(r2, recover).
random(r3, drug).

% Probability atoms
&pratom(r1, male(B), "1/2").
&pratom(r2, recover(B), "0.6") :- male(B), drug(B).
&pratom(r2, recover(B), "0.7") :- male(B), -drug(B).
&pratom(r2, recover(B), "0.2") :- -male(B), drug(B).
&pratom(r2, recover(B), "0.3") :- -male(B), -drug(B).
&pratom(r3, drug(B), "0.75") :- male(B).
&pratom(r3, drug(B), "0.25") :- -male(B).

% Observations and actions
do(drug(t)).

#show male/1.
#show recover/1.
#show drug/1.