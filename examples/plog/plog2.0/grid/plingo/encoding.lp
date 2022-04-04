% Sorts
#const m = 2.
#const n = 2.
node((1..m,1..n)).
boolean(true;false).

% Attributes
% faulty: #node -> #boolean.
% Statements
&random(N) { faulty(N,B) : boolean(B) } :- node(N).
#show faulty/2.

&pr(N) { faulty(N,true) } = "1/10" :- node(N).

% Information flows from node (X,Y) to (X+1,Y) and (X,Y+1) starting from node (1,1)
flow((1,1)) :- not faulty((1,1), true).
flow(N) :- rightof(N1,N), flow(N1), not faulty(N1, true).
flow(N) :- belowof(N1,N), flow(N1), not faulty(N1, true).

#show flow/1.
&query(flow((m,n))).
