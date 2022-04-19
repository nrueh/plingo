:- ['kb_smokes'].
people([p1,p3,p4]).
evidence(cancer(p1),false).
query(smokes(p1)).
evidence(smokes(p3),false).
evidence(cancer(p3),false).
evidence(smokes(p4),false).
evidence(cancer(p4),false).
friend(p1,p4).
friend(p4,p1).
friend(p1,p3).
friend(p3,p1).