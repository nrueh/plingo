% Sorts
#const m=2.
#const n=2.
node((1..m,1..n)).
boolean(true;false).

% Attributes
% faulty: #node -> #boolean.
% Statements
&random(N) { faulty(N,B) : boolean(B) } :- node(N).
#show faulty/2.

&pr(N) { faulty(N,true) } = "1/10" :- node(N).

% Information flows from node (X,Y) to (X+1,Y) and (X,Y+1) starting from node (1,1)
flow(1,1) :- not faulty((1,1), true).
flow(X,Y) :- node((X,Y)), flow(X-1,Y), not faulty((X-1,Y), true).
flow(X,Y) :- node((X,Y)), flow(X,Y-1), not faulty((X,Y-1), true).

% flow(X+1,Y) :- flow(X,Y), node((X+1,Y)), faulty((X,Y), false).
% flow(X,Y+1) :- flow(X,Y), node((X,Y+1)), faulty((X,Y), false).
#show flow/2.
&query(flow(m,n)).

% connected((X1,Y),(X2,Y)) :- node((X1,Y)), node((X2,Y)), X2-X1=1, not faulty((X1,Y),true).
% connected((X,Y1),(X,Y2)) :- node((X,Y1)), node((X,Y2)), Y2-Y1=1, not faulty((X,Y1),true).

% connected(N1,N3) :- connected(N1,N2), connected(N2,N3).

% &query(connected((1,1),(m,n))).
