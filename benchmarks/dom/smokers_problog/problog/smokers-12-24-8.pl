:- ['kb_smokes'].
people([p1,p11,p12,p2,p3,p4,p6,p7,p8,p9]).
query(smokes(p1)).
query(cancer(p1)).
evidence(smokes(p11),false).
query(cancer(p11)).
evidence(smokes(p12),true).
evidence(cancer(p12),false).
evidence(smokes(p2),true).
evidence(cancer(p2),false).
evidence(smokes(p3),true).
query(cancer(p3)).
evidence(smokes(p4),true).
evidence(cancer(p4),false).
evidence(smokes(p6),false).
evidence(cancer(p6),true).
query(smokes(p7)).
query(cancer(p7)).
query(smokes(p8)).
query(cancer(p8)).
evidence(smokes(p9),false).
query(cancer(p9)).
friend(p7,p9).
friend(p9,p7).
friend(p7,p8).
friend(p8,p7).
friend(p9,p12).
friend(p12,p9).
friend(p2,p8).
friend(p8,p2).
friend(p1,p2).
friend(p2,p1).
friend(p6,p11).
friend(p11,p6).
friend(p2,p4).
friend(p4,p2).
friend(p3,p11).
friend(p11,p3).
friend(p4,p12).
friend(p12,p4).
friend(p6,p7).
friend(p7,p6).
friend(p3,p8).
friend(p8,p3).
friend(p1,p8).
friend(p8,p1).
friend(p2,p7).
friend(p7,p2).
friend(p1,p4).
friend(p4,p1).