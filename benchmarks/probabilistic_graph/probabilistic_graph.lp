path(X,Y) :- edge(X,Y).
path(X,Y) :- edge(X,Z), path(Z,Y), Y != Z.
#show path/2.