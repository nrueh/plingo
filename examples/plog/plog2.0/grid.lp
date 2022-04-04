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

#show flow/2.
&query(flow(m,n)).
