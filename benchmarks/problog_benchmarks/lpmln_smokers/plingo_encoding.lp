cancer(X) :- smokes(X), &problog("3/4").
smokes(Y) :- smokes(X), influences(X, Y), &problog("4/5").

{smokes(X)} :- person(X).
{cancer(X)} :- person(X).
