% Pool: rule 'grid((1;2;3), (1;2;3))' can be converted like this. Bind pool to variables (also works with intervals)
% grid(Pool1,Pool2) :- Pool1=(1;2;3), Pool2=(1;2;3).


% Interval and Aggregate (converting interval leads to undesired results)
% {m(1..3) } = 1.

% This only has one model in LPMLN, rule is unsatisfied because 'unsat :- not {a}.' is always true.
% Should choice rules be converted? They are already functioning similar to LPMLN in the sense that they are optional
% {a} = 1.
% { a; b } = 1 :- c.
% c.
% b :- &weight(1).
% :~ a. [5@4]
% a :- b.
% c :- a.
% :~c. [5@4]
% This has the conversion
% unsat(0, "alpha") :- not {a≠.
% {a} :- not unsat(0,"alpha").
% :~ unsat(0,"alpha")

%What about the following aggregate?
% {a;b;c} = 2.

% Intervals. Does it even make sense to apply LPMLN to these rules? 
% size(2).
% grid(1..S,1..S) :- size(S).


% unsat(0, "alpha",(1;2;3),(1;2;3)) :- not  grid((1;2;3),(1;2;3))
% unsat(0,"alpha", X, Y):-not grid(X,Y), X=(1;2;3), Y=(1;2;3).
% grid(X,Y):-not unsat(0,"alpha",X,Y).
% :~unsat(0,"alpha",X,Y).[1@1]

% a :- &log("0.4").


