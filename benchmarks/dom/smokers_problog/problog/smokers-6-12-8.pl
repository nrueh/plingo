:- ['kb_smokes'].
people([p1,p2,p4,p5]).
query(smokes(p1)).
query(cancer(p1)).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(cancer(p4),false).
query(smokes(p4)).
evidence(smokes(p5),false).
evidence(cancer(p5),true).
friend(p1,p2).
friend(p2,p1).
friend(p4,p5).
friend(p5,p4).
friend(p1,p4).
friend(p4,p1).
