:- ['kb_smokes'].
people([p1,p10,p11,p12,p13,p15,p16,p17,p18,p2,p20,p21,p22,p23,p24,p27,p28,p29,p3,p30,p31,p32,p33,p34,p35,p36,p37,p38,p4,p5,p6,p7,p8,p9]).
evidence(cancer(p1),false).
query(smokes(p1)).
evidence(cancer(p10),true).
query(smokes(p10)).
query(smokes(p11)).
query(cancer(p11)).
query(smokes(p12)).
query(cancer(p12)).
evidence(smokes(p13),false).
evidence(cancer(p13),false).
evidence(smokes(p15),true).
evidence(cancer(p15),false).
query(smokes(p16)).
query(cancer(p16)).
query(smokes(p17)).
query(cancer(p17)).
query(smokes(p18)).
query(cancer(p18)).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(smokes(p20),false).
evidence(cancer(p20),false).
evidence(smokes(p21),false).
query(cancer(p21)).
evidence(cancer(p22),false).
query(smokes(p22)).
evidence(smokes(p23),false).
query(cancer(p23)).
evidence(cancer(p24),false).
query(smokes(p24)).
query(smokes(p27)).
query(cancer(p27)).
evidence(smokes(p28),false).
query(cancer(p28)).
evidence(smokes(p29),false).
query(cancer(p29)).
evidence(cancer(p3),true).
query(smokes(p3)).
evidence(smokes(p30),false).
query(cancer(p30)).
query(smokes(p31)).
query(cancer(p31)).
query(smokes(p32)).
query(cancer(p32)).
evidence(smokes(p33),false).
evidence(cancer(p33),false).
query(smokes(p34)).
query(cancer(p34)).
query(smokes(p35)).
query(cancer(p35)).
query(smokes(p36)).
query(cancer(p36)).
query(smokes(p37)).
query(cancer(p37)).
evidence(cancer(p38),false).
query(smokes(p38)).
query(smokes(p4)).
query(cancer(p4)).
evidence(smokes(p5),true).
evidence(cancer(p5),true).
evidence(cancer(p6),false).
query(smokes(p6)).
evidence(smokes(p7),true).
evidence(cancer(p7),true).
evidence(cancer(p8),false).
query(smokes(p8)).
evidence(smokes(p9),true).
evidence(cancer(p9),false).
friend(p20,p29).
friend(p29,p20).
friend(p9,p18).
friend(p18,p9).
friend(p3,p4).
friend(p4,p3).
friend(p11,p16).
friend(p16,p11).
friend(p11,p21).
friend(p21,p11).
friend(p28,p36).
friend(p36,p28).
friend(p10,p35).
friend(p35,p10).
friend(p7,p9).
friend(p9,p7).
friend(p4,p24).
friend(p24,p4).
friend(p7,p8).
friend(p8,p7).
friend(p9,p12).
friend(p12,p9).
friend(p16,p21).
friend(p21,p16).
friend(p6,p16).
friend(p16,p6).
friend(p13,p32).
friend(p32,p13).
friend(p7,p22).
friend(p22,p7).
friend(p11,p22).
friend(p22,p11).
friend(p4,p23).
friend(p23,p4).
friend(p17,p38).
friend(p38,p17).
friend(p4,p11).
friend(p11,p4).
friend(p17,p35).
friend(p35,p17).
friend(p31,p35).
friend(p35,p31).
friend(p8,p20).
friend(p20,p8).
friend(p1,p2).
friend(p2,p1).
friend(p4,p22).
friend(p22,p4).
friend(p2,p3).
friend(p3,p2).
friend(p2,p17).
friend(p17,p2).
friend(p23,p37).
friend(p37,p23).
friend(p5,p8).
friend(p8,p5).
friend(p10,p16).
friend(p16,p10).
friend(p11,p23).
friend(p23,p11).
friend(p17,p34).
friend(p34,p17).
friend(p10,p11).
friend(p11,p10).
friend(p4,p27).
friend(p27,p4).
friend(p30,p36).
friend(p36,p30).
friend(p30,p35).
friend(p35,p30).
friend(p6,p7).
friend(p7,p6).
friend(p15,p17).
friend(p17,p15).
friend(p12,p31).
friend(p31,p12).
friend(p11,p31).
friend(p31,p11).
friend(p1,p8).
friend(p8,p1).
friend(p3,p9).
friend(p9,p3).
friend(p27,p29).
friend(p29,p27).
friend(p3,p10).
friend(p10,p3).
friend(p13,p24).
friend(p24,p13).
friend(p1,p29).
friend(p29,p1).
friend(p12,p20).
friend(p20,p12).
friend(p2,p7).
friend(p7,p2).
friend(p12,p13).
friend(p13,p12).
friend(p3,p22).
friend(p22,p3).
friend(p15,p16).
friend(p16,p15).
friend(p8,p9).
friend(p9,p8).
friend(p23,p33).
friend(p33,p23).
friend(p29,p34).
friend(p34,p29).
friend(p2,p13).
friend(p13,p2).
friend(p29,p30).
friend(p30,p29).
friend(p4,p8).
friend(p8,p4).
friend(p1,p10).
friend(p10,p1).