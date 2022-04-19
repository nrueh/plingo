#const m=2.
#const n=2.
node((1..m,1..n)).

faulty(N) :- node(N), &problog("1/10").

% Information flows from node (X-1,Y) and (X,Y-1) to (X,Y) starting from node (1,1)
flow(1,1) :- not faulty((1,1)).
flow(X,Y) :- node((X,Y)), flow(X-1,Y), not faulty((X-1,Y)).
flow(X,Y) :- node((X,Y)), flow(X,Y-1), not faulty((X,Y-1)).

#show flow/2.
&query(flow(m,n)).
