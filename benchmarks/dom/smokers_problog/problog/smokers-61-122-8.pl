:- ['kb_smokes'].
people([p1,p10,p11,p12,p13,p14,p15,p16,p17,p18,p19,p2,p20,p21,p22,p24,p25,p26,p27,p28,p29,p3,p30,p31,p32,p33,p34,p35,p36,p37,p38,p39,p4,p40,p41,p42,p43,p44,p45,p46,p47,p48,p5,p50,p51,p52,p53,p54,p56,p57,p58,p59,p6,p60,p7,p8,p9]).
evidence(smokes(p1),false).
query(cancer(p1)).
evidence(smokes(p10),true).
evidence(cancer(p10),true).
query(smokes(p11)).
query(cancer(p11)).
query(smokes(p12)).
query(cancer(p12)).
evidence(cancer(p13),false).
query(smokes(p13)).
evidence(cancer(p14),false).
query(smokes(p14)).
evidence(smokes(p15),false).
evidence(cancer(p15),false).
query(smokes(p16)).
query(cancer(p16)).
evidence(smokes(p17),false).
query(cancer(p17)).
evidence(smokes(p18),false).
query(cancer(p18)).
evidence(smokes(p19),true).
query(cancer(p19)).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(smokes(p20),true).
query(cancer(p20)).
evidence(smokes(p21),false).
query(cancer(p21)).
evidence(smokes(p22),true).
query(cancer(p22)).
evidence(cancer(p24),false).
query(smokes(p24)).
evidence(smokes(p25),false).
evidence(cancer(p25),false).
query(smokes(p26)).
query(cancer(p26)).
evidence(cancer(p27),false).
query(smokes(p27)).
evidence(cancer(p28),false).
query(smokes(p28)).
evidence(smokes(p29),true).
evidence(cancer(p29),false).
evidence(cancer(p3),false).
query(smokes(p3)).
evidence(smokes(p30),true).
query(cancer(p30)).
evidence(cancer(p31),false).
query(smokes(p31)).
evidence(smokes(p32),false).
evidence(cancer(p32),false).
evidence(smokes(p33),false).
query(cancer(p33)).
query(smokes(p34)).
query(cancer(p34)).
query(smokes(p35)).
query(cancer(p35)).
evidence(cancer(p36),false).
query(smokes(p36)).
evidence(smokes(p37),false).
query(cancer(p37)).
evidence(smokes(p38),false).
query(cancer(p38)).
evidence(smokes(p39),false).
query(cancer(p39)).
evidence(cancer(p4),true).
query(smokes(p4)).
query(smokes(p40)).
query(cancer(p40)).
evidence(smokes(p41),false).
query(cancer(p41)).
evidence(smokes(p42),true).
query(cancer(p42)).
evidence(smokes(p43),false).
evidence(cancer(p43),false).
evidence(smokes(p44),true).
evidence(cancer(p44),true).
evidence(cancer(p45),false).
query(smokes(p45)).
evidence(cancer(p46),false).
query(smokes(p46)).
evidence(smokes(p47),false).
query(cancer(p47)).
query(smokes(p48)).
query(cancer(p48)).
evidence(smokes(p5),false).
query(cancer(p5)).
evidence(smokes(p50),false).
evidence(cancer(p50),false).
evidence(smokes(p51),true).
query(cancer(p51)).
evidence(cancer(p52),false).
query(smokes(p52)).
evidence(cancer(p53),false).
query(smokes(p53)).
evidence(cancer(p54),false).
query(smokes(p54)).
evidence(smokes(p56),false).
query(cancer(p56)).
evidence(smokes(p57),false).
evidence(cancer(p57),false).
evidence(smokes(p58),false).
query(cancer(p58)).
evidence(cancer(p59),false).
query(smokes(p59)).
evidence(cancer(p6),false).
query(smokes(p6)).
query(smokes(p60)).
query(cancer(p60)).
query(smokes(p7)).
query(cancer(p7)).
evidence(cancer(p8),false).
query(smokes(p8)).
evidence(smokes(p9),false).
query(cancer(p9)).
friend(p32,p44).
friend(p44,p32).
friend(p5,p7).
friend(p7,p5).
friend(p18,p26).
friend(p26,p18).
friend(p3,p4).
friend(p4,p3).
friend(p33,p37).
friend(p37,p33).
friend(p32,p41).
friend(p41,p32).
friend(p22,p44).
friend(p44,p22).
friend(p20,p22).
friend(p22,p20).
friend(p8,p13).
friend(p13,p8).
friend(p9,p15).
friend(p15,p9).
friend(p24,p58).
friend(p58,p24).
friend(p3,p60).
friend(p60,p3).
friend(p1,p11).
friend(p11,p1).
friend(p1,p31).
friend(p31,p1).
friend(p35,p57).
friend(p57,p35).
friend(p1,p3).
friend(p3,p1).
friend(p30,p60).
friend(p60,p30).
friend(p45,p46).
friend(p46,p45).
friend(p10,p38).
friend(p38,p10).
friend(p24,p28).
friend(p28,p24).
friend(p2,p10).
friend(p10,p2).
friend(p10,p40).
friend(p40,p10).
friend(p24,p47).
friend(p47,p24).
friend(p9,p13).
friend(p13,p9).
friend(p20,p59).
friend(p59,p20).
friend(p1,p22).
friend(p22,p1).
friend(p2,p6).
friend(p6,p2).
friend(p46,p53).
friend(p53,p46).
friend(p10,p27).
friend(p27,p10).
friend(p5,p36).
friend(p36,p5).
friend(p27,p58).
friend(p58,p27).
friend(p3,p11).
friend(p11,p3).
friend(p26,p31).
friend(p31,p26).
friend(p24,p41).
friend(p41,p24).
friend(p17,p25).
friend(p25,p17).
friend(p1,p18).
friend(p18,p1).
friend(p36,p58).
friend(p58,p36).
friend(p21,p35).
friend(p35,p21).
friend(p48,p53).
friend(p53,p48).
friend(p4,p38).
friend(p38,p4).
friend(p12,p30).
friend(p30,p12).
friend(p9,p32).
friend(p32,p9).
friend(p1,p24).
friend(p24,p1).
friend(p24,p46).
friend(p46,p24).
friend(p10,p14).
friend(p14,p10).
friend(p27,p30).
friend(p30,p27).
friend(p16,p17).
friend(p17,p16).
friend(p30,p38).
friend(p38,p30).
friend(p18,p52).
friend(p52,p18).
friend(p2,p36).
friend(p36,p2).
friend(p11,p45).
friend(p45,p11).
friend(p18,p48).
friend(p48,p18).
friend(p4,p33).
friend(p33,p4).
friend(p22,p51).
friend(p51,p22).
friend(p5,p24).
friend(p24,p5).
friend(p27,p57).
friend(p57,p27).
friend(p10,p43).
friend(p43,p10).
friend(p1,p17).
friend(p17,p1).
friend(p1,p7).
friend(p7,p1).
friend(p37,p43).
friend(p43,p37).
friend(p31,p54).
friend(p54,p31).
friend(p31,p34).
friend(p34,p31).
friend(p1,p6).
friend(p6,p1).
friend(p34,p42).
friend(p42,p34).
friend(p3,p16).
friend(p16,p3).
friend(p13,p39).
friend(p39,p13).
friend(p12,p42).
friend(p42,p12).
friend(p10,p12).
friend(p12,p10).
friend(p9,p16).
friend(p16,p9).
friend(p13,p31).
friend(p31,p13).
friend(p3,p9).
friend(p9,p3).
friend(p31,p46).
friend(p46,p31).
friend(p12,p16).
friend(p16,p12).
friend(p2,p40).
friend(p40,p2).
friend(p21,p56).
friend(p56,p21).
friend(p13,p58).
friend(p58,p13).
friend(p3,p27).
friend(p27,p3).
friend(p50,p52).
friend(p52,p50).
friend(p24,p25).
friend(p25,p24).
friend(p9,p35).
friend(p35,p9).
friend(p10,p29).
friend(p29,p10).
friend(p16,p18).
friend(p18,p16).
friend(p6,p12).
friend(p12,p6).
friend(p13,p20).
friend(p20,p13).
friend(p50,p54).
friend(p54,p50).
friend(p9,p33).
friend(p33,p9).
friend(p8,p37).
friend(p37,p8).
friend(p25,p36).
friend(p36,p25).
friend(p37,p38).
friend(p38,p37).
friend(p1,p45).
friend(p45,p1).
friend(p47,p51).
friend(p51,p47).
friend(p17,p47).
friend(p47,p17).
friend(p8,p36).
friend(p36,p8).
friend(p25,p26).
friend(p26,p25).
friend(p38,p46).
friend(p46,p38).
friend(p1,p9).
friend(p9,p1).
friend(p10,p46).
friend(p46,p10).
friend(p10,p17).
friend(p17,p10).
friend(p32,p33).
friend(p33,p32).
friend(p21,p50).
friend(p50,p21).
friend(p1,p4).
friend(p4,p1).
friend(p12,p32).
friend(p32,p12).
friend(p19,p34).
friend(p34,p19).
friend(p1,p36).
friend(p36,p1).