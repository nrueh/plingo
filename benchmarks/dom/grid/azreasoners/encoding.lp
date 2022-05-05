node((1..M,1..N)) :- m(M), n(N).

-2.19722 faulty(N) :- node(N).

% Information flows from node (X-1,Y) and (X,Y-1) to (X,Y) starting from node (1,1)
flow(1,1) :- not faulty((1,1)).
flow(X,Y) :- node((X,Y)), flow(X-1,Y), not faulty((X-1,Y)).
flow(X,Y) :- node((X,Y)), flow(X,Y-1), not faulty((X,Y-1)).

#show flow/2.
