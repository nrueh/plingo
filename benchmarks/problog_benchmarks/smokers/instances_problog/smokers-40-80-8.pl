:- ['kb_smokes'].
people([p1,p11,p12,p13,p14,p16,p17,p18,p19,p2,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p3,p30,p31,p32,p33,p34,p37,p38,p4,p40,p5,p6,p7,p8,p9]).
evidence(cancer(p1),true).
query(smokes(p1)).
evidence(smokes(p11),false).
evidence(cancer(p11),false).
evidence(smokes(p12),false).
evidence(cancer(p12),false).
evidence(smokes(p13),true).
evidence(cancer(p13),false).
evidence(smokes(p14),false).
query(cancer(p14)).
evidence(smokes(p16),false).
evidence(cancer(p16),false).
evidence(smokes(p17),false).
evidence(cancer(p17),false).
evidence(smokes(p18),false).
evidence(cancer(p18),false).
evidence(smokes(p19),true).
query(cancer(p19)).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(smokes(p20),true).
query(cancer(p20)).
query(smokes(p21)).
query(cancer(p21)).
query(smokes(p22)).
query(cancer(p22)).
evidence(smokes(p23),false).
evidence(cancer(p23),true).
evidence(smokes(p24),false).
evidence(cancer(p24),false).
evidence(smokes(p25),true).
query(cancer(p25)).
query(smokes(p26)).
query(cancer(p26)).
evidence(smokes(p27),false).
query(cancer(p27)).
evidence(cancer(p28),true).
query(smokes(p28)).
query(smokes(p29)).
query(cancer(p29)).
query(smokes(p3)).
query(cancer(p3)).
evidence(cancer(p30),false).
query(smokes(p30)).
evidence(cancer(p31),false).
query(smokes(p31)).
evidence(cancer(p32),false).
query(smokes(p32)).
evidence(smokes(p33),false).
evidence(cancer(p33),false).
evidence(smokes(p34),true).
evidence(cancer(p34),true).
evidence(smokes(p37),false).
evidence(cancer(p37),true).
evidence(smokes(p38),true).
evidence(cancer(p38),true).
query(smokes(p4)).
query(cancer(p4)).
evidence(smokes(p40),false).
evidence(cancer(p40),false).
evidence(smokes(p5),false).
query(cancer(p5)).
evidence(cancer(p6),true).
query(smokes(p6)).
query(smokes(p7)).
query(cancer(p7)).
query(smokes(p8)).
query(cancer(p8)).
evidence(smokes(p9),true).
query(cancer(p9)).
friend(p3,p4).
friend(p4,p3).
friend(p4,p13).
friend(p13,p4).
friend(p14,p19).
friend(p19,p14).
friend(p4,p9).
friend(p9,p4).
friend(p7,p14).
friend(p14,p7).
friend(p4,p32).
friend(p32,p4).
friend(p12,p19).
friend(p19,p12).
friend(p16,p22).
friend(p22,p16).
friend(p13,p17).
friend(p17,p13).
friend(p6,p26).
friend(p26,p6).
friend(p12,p17).
friend(p17,p12).
friend(p2,p12).
friend(p12,p2).
friend(p7,p8).
friend(p8,p7).
friend(p21,p37).
friend(p37,p21).
friend(p6,p27).
friend(p27,p6).
friend(p16,p19).
friend(p19,p16).
friend(p12,p33).
friend(p33,p12).
friend(p31,p37).
friend(p37,p31).
friend(p9,p13).
friend(p13,p9).
friend(p3,p19).
friend(p19,p3).
friend(p21,p22).
friend(p22,p21).
friend(p1,p32).
friend(p32,p1).
friend(p1,p22).
friend(p22,p1).
friend(p17,p40).
friend(p40,p17).
friend(p1,p2).
friend(p2,p1).
friend(p2,p4).
friend(p4,p2).
friend(p3,p11).
friend(p11,p3).
friend(p26,p28).
friend(p28,p26).
friend(p2,p18).
friend(p18,p2).
friend(p29,p38).
friend(p38,p29).
friend(p9,p30).
friend(p30,p9).
friend(p22,p31).
friend(p31,p22).
friend(p19,p20).
friend(p20,p19).
friend(p16,p17).
friend(p17,p16).
friend(p1,p12).
friend(p12,p1).
friend(p8,p11).
friend(p11,p8).
friend(p2,p9).
friend(p9,p2).
friend(p17,p22).
friend(p22,p17).
friend(p12,p23).
friend(p23,p12).
friend(p25,p28).
friend(p28,p25).
friend(p21,p27).
friend(p27,p21).
friend(p9,p14).
friend(p14,p9).
friend(p12,p22).
friend(p22,p12).
friend(p2,p22).
friend(p22,p2).
friend(p12,p16).
friend(p16,p12).
friend(p2,p24).
friend(p24,p2).
friend(p3,p27).
friend(p27,p3).
friend(p8,p21).
friend(p21,p8).
friend(p5,p22).
friend(p22,p5).
friend(p2,p21).
friend(p21,p2).
friend(p2,p14).
friend(p14,p2).
friend(p26,p37).
friend(p37,p26).
friend(p3,p23).
friend(p23,p3).
friend(p12,p14).
friend(p14,p12).
friend(p24,p27).
friend(p27,p24).
friend(p27,p40).
friend(p40,p27).
friend(p22,p33).
friend(p33,p22).
friend(p13,p28).
friend(p28,p13).
friend(p12,p18).
friend(p18,p12).
friend(p29,p34).
friend(p34,p29).
friend(p3,p32).
friend(p32,p3).
friend(p1,p9).
friend(p9,p1).
friend(p32,p33).
friend(p33,p32).
friend(p1,p4).
friend(p4,p1).
friend(p19,p34).
friend(p34,p19).
friend(p3,p18).
friend(p18,p3).
friend(p14,p17).
friend(p17,p14).