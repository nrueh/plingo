{in(X)} :- node(X).
disconnected(X, Y) :- in(X), in(Y), not edge(X, Y).
:- not in(X), node(X), &weight(5).
:- disconnected(X, Y), &weight(5).