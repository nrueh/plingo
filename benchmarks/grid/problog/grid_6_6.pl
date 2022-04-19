node((1,1)).
node((1,2)).
node((1,3)).
node((1,4)).
node((1,5)).
node((1,6)).
node((2,1)).
node((2,2)).
node((2,3)).
node((2,4)).
node((2,5)).
node((2,6)).
node((3,1)).
node((3,2)).
node((3,3)).
node((3,4)).
node((3,5)).
node((3,6)).
node((4,1)).
node((4,2)).
node((4,3)).
node((4,4)).
node((4,5)).
node((4,6)).
node((5,1)).
node((5,2)).
node((5,3)).
node((5,4)).
node((5,5)).
node((5,6)).
node((6,1)).
node((6,2)).
node((6,3)).
node((6,4)).
node((6,5)).
node((6,6)).

0.1::faulty(N) :- node(N).

% Information flows from node (X,Y) to (X+1,Y) and (X,Y+1) starting from node (1,1)
flow(1,1) :- not faulty((1,1)).
flow(X,Y) :- node((X,Y)), flow(X1,Y), not faulty((X1,Y)), X1 is X-1.
flow(X,Y) :- node((X,Y)), flow(X,Y1), not faulty((X,Y1)), Y1 is Y-1.

query(flow(6,6)).
