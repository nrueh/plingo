node((1,1)).
node((1,2)).
node((2,1)).
node((2,2)).
node((3,1)).
node((3,2)).
node((4,1)).
node((4,2)).
node((5,1)).
node((5,2)).
node((6,1)).
node((6,2)).
node((7,1)).
node((7,2)).
node((8,1)).
node((8,2)).
node((9,1)).
node((9,2)).
node((10,1)).
node((10,2)).

0.1::faulty(N) :- node(N).

% Information flows from node (X,Y) to (X+1,Y) and (X,Y+1) starting from node (1,1)
flow(1,1) :- not faulty((1,1)).
flow(X,Y) :- node((X,Y)), flow(X1,Y), not faulty((X1,Y)), X1 is X-1.
flow(X,Y) :- node((X,Y)), flow(X,Y1), not faulty((X,Y1)), Y1 is Y-1.

query(flow(10,2)).
