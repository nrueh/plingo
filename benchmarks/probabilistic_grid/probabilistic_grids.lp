path(X,Y) :- edge(X,Y).
path(X,Y) :- edge(X,Z), path(Z,Y).
#show path/2.