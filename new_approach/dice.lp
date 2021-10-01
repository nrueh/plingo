% sorts
dice(d1;d2).
score(1..6).
person(mike,john).

% statements

owns(d1,mike).
owns(d2,john).


% random rules 

&random{ r1; roll(D,X) : score(X) } :- dice(D).

% probability atoms
&pr{ r1; roll(D,X) } = "1/6"  :- owns(D,john), score(X).
&pr{ r1; roll(D,6) } = "1/4"  :- owns(D,mike).
&pr{ r1; roll(D,X) } = "3/20"  :- owns(D,mike), score(X), X != 6.

% _pr(r1,(roll,D,X),"1/6") :- owns(D,john), score(X).
% _pr(r1,(roll,D,6),"1/4") :- owns(D,mike).
% _pr(r1,(roll,D,X),"3/20") :- X !=6, score(X), owns(D,mike).

% &obs { roll(d2,1) }.
% _obs((roll,d2,1)).

% &do { roll(d1,1) }.
% _do((roll,d1,1)).

