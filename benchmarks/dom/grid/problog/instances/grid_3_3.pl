node((1,1)).
node((1,2)).
node((1,3)).
node((2,1)).
node((2,2)).
node((2,3)).
node((3,1)).
node((3,2)).
node((3,3)).

0.1::faulty(N) :- node(N).

% Information flows from node (X-1,Y) and (X,Y-1) to (X,Y) starting from node (1,1)
flow(1,1) :- not faulty((1,1)).
flow(X,Y) :- node((X,Y)), flow(X1,Y), not faulty((X1,Y)), X1 is X-1.
flow(X,Y) :- node((X,Y)), flow(X,Y1), not faulty((X,Y1)), Y1 is Y-1.

query:-flow(3,3).
query(query).
