stress(P) :- person(P), &weight(log(0.2)).
influences(P1, P2) :- friend(P1,P2), &weight(log(0.3)).
cancer_spont(P) :- person(P), &weight(log(0.1)).
cancer_smoke(P) :- person(P), &weight(log(0.3)).

smokes(X) :- stress(X).

smokes(X) :- smokes(Y), influences(X,Y).
cancer(P) :- cancer_spont(P).
cancer(P) :- smokes(P), cancer_smoke(P).