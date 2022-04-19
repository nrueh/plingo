:- ['kb_smokes'].
people([p1,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p2,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p3,p31,p32,p33,p34,p35,p36,p37,p39,p4,p40,p41,p42,p43,p5,p6,p7,p8,p9]).
evidence(smokes(p1),true).
query(cancer(p1)).
evidence(cancer(p10),true).
query(smokes(p10)).
evidence(cancer(p11),false).
query(smokes(p11)).
query(smokes(p12)).
query(cancer(p12)).
evidence(cancer(p13),false).
query(smokes(p13)).
evidence(smokes(p14),true).
evidence(cancer(p14),false).
evidence(cancer(p15),true).
query(smokes(p15)).
query(smokes(p16)).
query(cancer(p16)).
evidence(smokes(p17),true).
evidence(cancer(p17),false).
evidence(smokes(p18),false).
evidence(cancer(p18),false).
query(smokes(p19)).
query(cancer(p19)).
evidence(smokes(p2),true).
evidence(cancer(p2),false).
evidence(cancer(p20),false).
query(smokes(p20)).
evidence(smokes(p21),false).
query(cancer(p21)).
evidence(smokes(p22),true).
evidence(cancer(p22),false).
evidence(smokes(p23),false).
query(cancer(p23)).
evidence(smokes(p24),true).
query(cancer(p24)).
evidence(smokes(p25),false).
query(cancer(p25)).
evidence(smokes(p26),false).
query(cancer(p26)).
query(smokes(p27)).
query(cancer(p27)).
evidence(smokes(p28),false).
evidence(cancer(p28),false).
query(smokes(p29)).
query(cancer(p29)).
query(smokes(p3)).
query(cancer(p3)).
query(smokes(p31)).
query(cancer(p31)).
evidence(cancer(p32),false).
query(smokes(p32)).
evidence(cancer(p33),false).
query(smokes(p33)).
evidence(smokes(p34),true).
evidence(cancer(p34),false).
evidence(smokes(p35),true).
query(cancer(p35)).
evidence(smokes(p36),false).
query(cancer(p36)).
query(smokes(p37)).
query(cancer(p37)).
evidence(smokes(p39),true).
query(cancer(p39)).
evidence(cancer(p4),false).
query(smokes(p4)).
evidence(smokes(p40),false).
query(cancer(p40)).
evidence(smokes(p41),false).
query(cancer(p41)).
evidence(cancer(p42),true).
query(smokes(p42)).
query(smokes(p43)).
query(cancer(p43)).
evidence(smokes(p5),false).
query(cancer(p5)).
query(smokes(p6)).
query(cancer(p6)).
evidence(smokes(p7),false).
query(cancer(p7)).
evidence(cancer(p8),false).
query(smokes(p8)).
evidence(smokes(p9),false).
evidence(cancer(p9),false).
friend(p14,p25).
friend(p25,p14).
friend(p13,p19).
friend(p19,p13).
friend(p34,p35).
friend(p35,p34).
friend(p7,p25).
friend(p25,p7).
friend(p17,p27).
friend(p27,p17).
friend(p12,p17).
friend(p17,p12).
friend(p7,p8).
friend(p8,p7).
friend(p24,p28).
friend(p28,p24).
friend(p1,p39).
friend(p39,p1).
friend(p4,p10).
friend(p10,p4).
friend(p18,p35).
friend(p35,p18).
friend(p23,p32).
friend(p32,p23).
friend(p5,p27).
friend(p27,p5).
friend(p4,p37).
friend(p37,p4).
friend(p19,p39).
friend(p39,p19).
friend(p16,p43).
friend(p43,p16).
friend(p6,p28).
friend(p28,p6).
friend(p1,p2).
friend(p2,p1).
friend(p1,p13).
friend(p13,p1).
friend(p13,p35).
friend(p35,p13).
friend(p16,p32).
friend(p32,p16).
friend(p19,p36).
friend(p36,p19).
friend(p23,p37).
friend(p37,p23).
friend(p21,p24).
friend(p24,p21).
friend(p7,p27).
friend(p27,p7).
friend(p24,p31).
friend(p31,p24).
friend(p28,p37).
friend(p37,p28).
friend(p2,p35).
friend(p35,p2).
friend(p4,p27).
friend(p27,p4).
friend(p17,p21).
friend(p21,p17).
friend(p19,p20).
friend(p20,p19).
friend(p8,p33).
friend(p33,p8).
friend(p3,p14).
friend(p14,p3).
friend(p17,p29).
friend(p29,p17).
friend(p4,p26).
friend(p26,p4).
friend(p17,p18).
friend(p18,p17).
friend(p27,p34).
friend(p34,p27).
friend(p33,p34).
friend(p34,p33).
friend(p35,p41).
friend(p41,p35).
friend(p6,p39).
friend(p39,p6).
friend(p1,p6).
friend(p6,p1).
friend(p34,p42).
friend(p42,p34).
friend(p12,p21).
friend(p21,p12).
friend(p4,p5).
friend(p5,p4).
friend(p28,p39).
friend(p39,p28).
friend(p10,p18).
friend(p18,p10).
friend(p6,p24).
friend(p24,p6).
friend(p10,p29).
friend(p29,p10).
friend(p16,p18).
friend(p18,p16).
friend(p2,p7).
friend(p7,p2).
friend(p24,p40).
friend(p40,p24).
friend(p27,p40).
friend(p40,p27).
friend(p6,p13).
friend(p13,p6).
friend(p15,p37).
friend(p37,p15).
friend(p5,p10).
friend(p10,p5).
friend(p12,p18).
friend(p18,p12).
friend(p10,p22).
friend(p22,p10).
friend(p16,p39).
friend(p39,p16).
friend(p21,p43).
friend(p43,p21).
friend(p11,p20).
friend(p20,p11).
friend(p25,p26).
friend(p26,p25).
friend(p17,p39).
friend(p39,p17).
friend(p9,p31).
friend(p31,p9).
friend(p9,p10).
friend(p10,p9).
friend(p22,p32).
friend(p32,p22).
friend(p39,p42).
friend(p42,p39).
friend(p14,p17).
friend(p17,p14).
friend(p1,p5).
friend(p5,p1).