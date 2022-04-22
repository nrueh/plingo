1.1 cancer(X) :- smokes(X).
1.5 smokes(Y) :- smokes(X), influences(X, Y).

{smokes(X)} :- person(X).
{cancer(X)} :- person(X).

#show .
