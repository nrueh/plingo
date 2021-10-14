% Sorts
patch(p1; p2).
day(1..5).
boolean(t;f).

% Regular part
found(P, D, f) :- not found(P, D, t), patch(P), day(D).

% Random rules
&random { hidden_in(P) : patch(P) }.
&random { found(P, D, B) : boolean(B) } :- hidden_in(P), look(D, P).

% Probability
&pr { hidden_in(p1) } = "0.8".
&pr { found(P, D, t) } = "0.2" :- patch(P), day(D).

% Day 1
look(1, p1).

% Day 2
&obs { found(p1, 1, f) }.
look(2, p1).

found(P, D) :- found(P, D, t).

#show hidden_in/1.
#show found/2.
