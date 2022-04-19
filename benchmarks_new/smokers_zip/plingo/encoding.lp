person(P) :- people(P).

stress(P) :- person(P), &problog("0.2").
influences(P1,P2) :- friend(P1,P2), &problog("0.3").
cancer_prior(P) :- person(P), &problog("0.1").
cancer_smokes(P) :- person(P), smokes(P), &problog("0.3").

smokes(P) :- stress(P).
smokes(P2) :- smokes(P1), influences(P1,P2).
cancer(P) :- cancer_prior(P).
cancer(P) :- smokes(P), cancer_smokes(P).

#show smokes/1.
#show cancer/1.
#show stress/1.
