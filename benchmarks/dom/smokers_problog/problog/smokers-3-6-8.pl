:- ['kb_smokes'].
people([p1,p2,p3]).
evidence(cancer(p1),false).
query(smokes(p1)).
evidence(smokes(p2),false).
evidence(cancer(p2),false).
evidence(smokes(p3),false).
evidence(cancer(p3),false).
friend(p2,p3).
friend(p3,p2).
friend(p1,p2).
friend(p2,p1).
