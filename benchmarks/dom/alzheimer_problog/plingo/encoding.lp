p(X,Y) :- drc(X,Y).
p(X,Y) :- drc(X, Z), Z != Y, p(Z, Y).
