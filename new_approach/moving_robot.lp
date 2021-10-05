% Sorts
time(0;1).
rooms(r0;r1;r2).

% Regular part
in(1, R) :- go_in(R), not ab.
ab :- break.

in(1, R) :- in(0, R), not -in(1, R).
-in(1, R) :- -in(0, R), not in(1, R), rooms(R).

open(R) :- not -open(R), rooms(R).

% Random rules
&random(r1) { in(1, R) : open(R) } :- go_in(R1), break.

go_in(r0).
break.
-open(r2).
#show in/2.
