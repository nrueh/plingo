{in(X)} :- node(X).
disconnected(X, Y) :- in(X), in(Y), not edge(X, Y).
:~ not in(X), node(X).[5,3,(X,)]
:~ disconnected(X, Y).[5,4,(X,Y,)]