:- ['kb_smokes'].
people([p1,p10,p11,p12,p13,p15,p16,p17,p18,p19,p2,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p3,p30,p31,p32,p33,p34,p35,p36,p37,p39,p4,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p5,p50,p51,p52,p53,p54,p55,p56,p58,p59,p6,p60,p63,p64,p65,p67,p68,p7,p70,p72,p73,p74,p75,p8,p9]).
evidence(smokes(p1),false).
evidence(cancer(p1),false).
evidence(cancer(p10),true).
query(smokes(p10)).
evidence(smokes(p11),false).
evidence(cancer(p11),true).
evidence(smokes(p12),false).
query(cancer(p12)).
evidence(cancer(p13),false).
query(smokes(p13)).
evidence(smokes(p15),true).
query(cancer(p15)).
evidence(cancer(p16),false).
query(smokes(p16)).
query(smokes(p17)).
query(cancer(p17)).
evidence(cancer(p18),false).
query(smokes(p18)).
evidence(smokes(p19),true).
query(cancer(p19)).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(smokes(p20),true).
query(cancer(p20)).
evidence(cancer(p21),false).
query(smokes(p21)).
evidence(smokes(p22),false).
evidence(cancer(p22),true).
evidence(smokes(p23),false).
evidence(cancer(p23),false).
query(smokes(p24)).
query(cancer(p24)).
query(smokes(p25)).
query(cancer(p25)).
query(smokes(p26)).
query(cancer(p26)).
evidence(smokes(p27),false).
evidence(cancer(p27),false).
evidence(smokes(p28),false).
query(cancer(p28)).
evidence(smokes(p29),false).
evidence(cancer(p29),false).
query(smokes(p3)).
query(cancer(p3)).
evidence(smokes(p30),false).
evidence(cancer(p30),false).
query(smokes(p31)).
query(cancer(p31)).
evidence(cancer(p32),true).
query(smokes(p32)).
evidence(cancer(p33),true).
query(smokes(p33)).
evidence(smokes(p34),true).
query(cancer(p34)).
query(smokes(p35)).
query(cancer(p35)).
evidence(cancer(p36),false).
query(smokes(p36)).
evidence(smokes(p37),false).
query(cancer(p37)).
evidence(smokes(p39),true).
evidence(cancer(p39),true).
query(smokes(p4)).
query(cancer(p4)).
evidence(smokes(p40),true).
query(cancer(p40)).
query(smokes(p41)).
query(cancer(p41)).
evidence(cancer(p42),false).
query(smokes(p42)).
query(smokes(p43)).
query(cancer(p43)).
evidence(smokes(p44),true).
evidence(cancer(p44),false).
query(smokes(p45)).
query(cancer(p45)).
evidence(smokes(p46),false).
query(cancer(p46)).
evidence(cancer(p47),true).
query(smokes(p47)).
evidence(smokes(p48),true).
evidence(cancer(p48),false).
query(smokes(p49)).
query(cancer(p49)).
evidence(smokes(p5),true).
query(cancer(p5)).
evidence(smokes(p50),true).
query(cancer(p50)).
query(smokes(p51)).
query(cancer(p51)).
evidence(smokes(p52),false).
evidence(cancer(p52),false).
evidence(smokes(p53),false).
query(cancer(p53)).
query(smokes(p54)).
query(cancer(p54)).
evidence(smokes(p55),true).
evidence(cancer(p55),false).
evidence(cancer(p56),false).
query(smokes(p56)).
evidence(smokes(p58),true).
evidence(cancer(p58),false).
evidence(cancer(p59),false).
query(smokes(p59)).
evidence(smokes(p6),true).
query(cancer(p6)).
evidence(smokes(p60),true).
query(cancer(p60)).
evidence(cancer(p63),false).
query(smokes(p63)).
query(smokes(p64)).
query(cancer(p64)).
evidence(smokes(p65),true).
evidence(cancer(p65),false).
evidence(cancer(p67),false).
query(smokes(p67)).
evidence(cancer(p68),true).
query(smokes(p68)).
evidence(smokes(p7),false).
query(cancer(p7)).
evidence(cancer(p70),false).
query(smokes(p70)).
query(smokes(p72)).
query(cancer(p72)).
query(smokes(p73)).
query(cancer(p73)).
query(smokes(p74)).
query(cancer(p74)).
evidence(smokes(p75),false).
query(cancer(p75)).
evidence(smokes(p8),false).
evidence(cancer(p8),false).
evidence(smokes(p9),false).
query(cancer(p9)).
friend(p23,p46).
friend(p46,p23).
friend(p49,p50).
friend(p50,p49).
friend(p21,p30).
friend(p30,p21).
friend(p5,p67).
friend(p67,p5).
friend(p3,p4).
friend(p4,p3).
friend(p6,p55).
friend(p55,p6).
friend(p54,p55).
friend(p55,p54).
friend(p20,p48).
friend(p48,p20).
friend(p47,p67).
friend(p67,p47).
friend(p34,p35).
friend(p35,p34).
friend(p42,p50).
friend(p50,p42).
friend(p2,p11).
friend(p11,p2).
friend(p33,p70).
friend(p70,p33).
friend(p2,p44).
friend(p44,p2).
friend(p50,p56).
friend(p56,p50).
friend(p60,p63).
friend(p63,p60).
friend(p3,p60).
friend(p60,p3).
friend(p63,p72).
friend(p72,p63).
friend(p41,p43).
friend(p43,p41).
friend(p15,p48).
friend(p48,p15).
friend(p48,p50).
friend(p50,p48).
friend(p1,p11).
friend(p11,p1).
friend(p5,p65).
friend(p65,p5).
friend(p48,p58).
friend(p58,p48).
friend(p2,p12).
friend(p12,p2).
friend(p45,p46).
friend(p46,p45).
friend(p10,p23).
friend(p23,p10).
friend(p4,p10).
friend(p10,p4).
friend(p2,p10).
friend(p10,p2).
friend(p32,p64).
friend(p64,p32).
friend(p6,p27).
friend(p27,p6).
friend(p11,p22).
friend(p22,p11).
friend(p2,p31).
friend(p31,p2).
friend(p49,p58).
friend(p58,p49).
friend(p55,p64).
friend(p64,p55).
friend(p9,p13).
friend(p13,p9).
friend(p31,p35).
friend(p35,p31).
friend(p26,p27).
friend(p27,p26).
friend(p32,p49).
friend(p49,p32).
friend(p21,p22).
friend(p22,p21).
friend(p28,p75).
friend(p75,p28).
friend(p15,p55).
friend(p55,p15).
friend(p1,p2).
friend(p2,p1).
friend(p1,p51).
friend(p51,p1).
friend(p53,p59).
friend(p59,p53).
friend(p31,p59).
friend(p59,p31).
friend(p7,p17).
friend(p17,p7).
friend(p39,p40).
friend(p40,p39).
friend(p15,p26).
friend(p26,p15).
friend(p3,p11).
friend(p11,p3).
friend(p20,p40).
friend(p40,p20).
friend(p7,p42).
friend(p42,p7).
friend(p40,p53).
friend(p53,p40).
friend(p10,p16).
friend(p16,p10).
friend(p21,p24).
friend(p24,p21).
friend(p2,p43).
friend(p43,p2).
friend(p26,p74).
friend(p74,p26).
friend(p11,p23).
friend(p23,p11).
friend(p12,p52).
friend(p52,p12).
friend(p11,p13).
friend(p13,p11).
friend(p28,p63).
friend(p63,p28).
friend(p4,p27).
friend(p27,p4).
friend(p10,p21).
friend(p21,p10).
friend(p8,p17).
friend(p17,p8).
friend(p23,p27).
friend(p27,p23).
friend(p39,p49).
friend(p49,p39).
friend(p53,p73).
friend(p73,p53).
friend(p16,p44).
friend(p44,p16).
friend(p46,p50).
friend(p50,p46).
friend(p37,p67).
friend(p67,p37).
friend(p40,p60).
friend(p60,p40).
friend(p7,p32).
friend(p32,p7).
friend(p11,p30).
friend(p30,p11).
friend(p12,p23).
friend(p23,p12).
friend(p7,p26).
friend(p26,p7).
friend(p4,p43).
friend(p43,p4).
friend(p17,p18).
friend(p18,p17).
friend(p3,p13).
friend(p13,p3).
friend(p20,p68).
friend(p68,p20).
friend(p11,p70).
friend(p70,p11).
friend(p47,p48).
friend(p48,p47).
friend(p21,p65).
friend(p65,p21).
friend(p58,p60).
friend(p60,p58).
friend(p23,p59).
friend(p59,p23).
friend(p58,p67).
friend(p67,p58).
friend(p40,p45).
friend(p45,p40).
friend(p10,p41).
friend(p41,p10).
friend(p65,p70).
friend(p70,p65).
friend(p9,p26).
friend(p26,p9).
friend(p6,p15).
friend(p15,p6).
friend(p12,p16).
friend(p16,p12).
friend(p2,p40).
friend(p40,p2).
friend(p10,p19).
friend(p19,p10).
friend(p21,p23).
friend(p23,p21).
friend(p3,p39).
friend(p39,p3).
friend(p2,p74).
friend(p74,p2).
friend(p4,p42).
friend(p42,p4).
friend(p4,p5).
friend(p5,p4).
friend(p1,p29).
friend(p29,p1).
friend(p26,p30).
friend(p30,p26).
friend(p5,p51).
friend(p51,p5).
friend(p2,p41).
friend(p41,p2).
friend(p59,p60).
friend(p60,p59).
friend(p1,p40).
friend(p40,p1).
friend(p48,p59).
friend(p59,p48).
friend(p16,p18).
friend(p18,p16).
friend(p36,p56).
friend(p56,p36).
friend(p34,p67).
friend(p67,p34).
friend(p3,p22).
friend(p22,p3).
friend(p3,p41).
friend(p41,p3).
friend(p39,p47).
friend(p47,p39).
friend(p6,p8).
friend(p8,p6).
friend(p22,p26).
friend(p26,p22).
friend(p40,p49).
friend(p49,p40).
friend(p21,p29).
friend(p29,p21).
friend(p12,p18).
friend(p18,p12).
friend(p49,p68).
friend(p68,p49).
friend(p55,p73).
friend(p73,p55).
friend(p2,p20).
friend(p20,p2).
friend(p8,p9).
friend(p9,p8).
friend(p42,p47).
friend(p47,p42).
friend(p20,p58).
friend(p58,p20).
friend(p45,p72).
friend(p72,p45).
friend(p25,p26).
friend(p26,p25).
friend(p49,p53).
friend(p53,p49).
friend(p15,p50).
friend(p50,p15).
friend(p20,p25).
friend(p25,p20).
friend(p44,p65).
friend(p65,p44).
friend(p44,p55).
friend(p55,p44).
friend(p22,p39).
friend(p39,p22).
friend(p22,p23).
friend(p23,p22).
friend(p1,p4).
friend(p4,p1).