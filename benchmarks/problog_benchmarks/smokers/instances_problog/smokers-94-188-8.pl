:- ['kb_smokes'].
people([p1,p10,p11,p13,p14,p15,p16,p17,p18,p19,p2,p20,p21,p22,p23,p24,p25,p26,p27,p28,p29,p3,p31,p32,p33,p34,p36,p37,p38,p39,p4,p40,p41,p42,p43,p44,p45,p46,p47,p48,p49,p5,p50,p51,p52,p53,p54,p55,p56,p57,p58,p59,p6,p60,p61,p62,p63,p64,p65,p66,p67,p68,p69,p7,p70,p71,p72,p73,p74,p75,p76,p77,p78,p79,p8,p81,p83,p84,p85,p87,p88,p89,p9,p90,p91,p92,p93,p94]).
evidence(smokes(p1),false).
evidence(cancer(p1),false).
evidence(smokes(p10),true).
evidence(cancer(p10),false).
evidence(smokes(p11),false).
query(cancer(p11)).
evidence(smokes(p13),true).
query(cancer(p13)).
evidence(smokes(p14),false).
evidence(cancer(p14),false).
evidence(smokes(p15),true).
evidence(cancer(p15),false).
query(smokes(p16)).
query(cancer(p16)).
query(smokes(p17)).
query(cancer(p17)).
query(smokes(p18)).
query(cancer(p18)).
evidence(smokes(p19),true).
query(cancer(p19)).
evidence(smokes(p2),false).
evidence(cancer(p2),true).
query(smokes(p20)).
query(cancer(p20)).
query(smokes(p21)).
query(cancer(p21)).
evidence(cancer(p22),true).
query(smokes(p22)).
evidence(smokes(p23),true).
evidence(cancer(p23),false).
evidence(smokes(p24),true).
evidence(cancer(p24),false).
evidence(smokes(p25),true).
query(cancer(p25)).
evidence(smokes(p26),true).
query(cancer(p26)).
evidence(cancer(p27),false).
query(smokes(p27)).
evidence(cancer(p28),false).
query(smokes(p28)).
query(smokes(p29)).
query(cancer(p29)).
query(smokes(p3)).
query(cancer(p3)).
evidence(smokes(p31),true).
query(cancer(p31)).
evidence(smokes(p32),false).
evidence(cancer(p32),false).
evidence(cancer(p33),true).
query(smokes(p33)).
query(smokes(p34)).
query(cancer(p34)).
evidence(smokes(p36),true).
evidence(cancer(p36),false).
evidence(smokes(p37),false).
evidence(cancer(p37),false).
evidence(cancer(p38),true).
query(smokes(p38)).
evidence(cancer(p39),false).
query(smokes(p39)).
evidence(cancer(p4),false).
query(smokes(p4)).
query(smokes(p40)).
query(cancer(p40)).
evidence(smokes(p41),false).
evidence(cancer(p41),false).
evidence(cancer(p42),false).
query(smokes(p42)).
evidence(smokes(p43),false).
evidence(cancer(p43),false).
evidence(smokes(p44),false).
evidence(cancer(p44),false).
evidence(cancer(p45),false).
query(smokes(p45)).
evidence(smokes(p46),true).
query(cancer(p46)).
evidence(cancer(p47),false).
query(smokes(p47)).
query(smokes(p48)).
query(cancer(p48)).
evidence(cancer(p49),false).
query(smokes(p49)).
evidence(smokes(p5),true).
query(cancer(p5)).
evidence(smokes(p50),true).
evidence(cancer(p50),false).
query(smokes(p51)).
query(cancer(p51)).
evidence(smokes(p52),true).
evidence(cancer(p52),false).
query(smokes(p53)).
query(cancer(p53)).
query(smokes(p54)).
query(cancer(p54)).
query(smokes(p55)).
query(cancer(p55)).
query(smokes(p56)).
query(cancer(p56)).
query(smokes(p57)).
query(cancer(p57)).
evidence(smokes(p58),true).
query(cancer(p58)).
evidence(smokes(p59),true).
evidence(cancer(p59),false).
evidence(smokes(p6),true).
evidence(cancer(p6),false).
evidence(smokes(p60),true).
evidence(cancer(p60),false).
evidence(smokes(p61),true).
evidence(cancer(p61),false).
evidence(smokes(p62),false).
evidence(cancer(p62),true).
evidence(smokes(p63),false).
query(cancer(p63)).
evidence(smokes(p64),false).
query(cancer(p64)).
evidence(smokes(p65),false).
evidence(cancer(p65),false).
evidence(smokes(p66),true).
evidence(cancer(p66),false).
query(smokes(p67)).
query(cancer(p67)).
evidence(cancer(p68),false).
query(smokes(p68)).
query(smokes(p69)).
query(cancer(p69)).
evidence(cancer(p7),true).
query(smokes(p7)).
query(smokes(p70)).
query(cancer(p70)).
evidence(smokes(p71),true).
evidence(cancer(p71),false).
evidence(smokes(p72),false).
evidence(cancer(p72),false).
evidence(cancer(p73),false).
query(smokes(p73)).
evidence(smokes(p74),true).
query(cancer(p74)).
query(smokes(p75)).
query(cancer(p75)).
evidence(smokes(p76),true).
query(cancer(p76)).
evidence(cancer(p77),true).
query(smokes(p77)).
evidence(cancer(p78),false).
query(smokes(p78)).
evidence(smokes(p79),false).
evidence(cancer(p79),true).
evidence(cancer(p8),false).
query(smokes(p8)).
evidence(cancer(p81),false).
query(smokes(p81)).
evidence(cancer(p83),true).
query(smokes(p83)).
evidence(cancer(p84),true).
query(smokes(p84)).
evidence(cancer(p85),true).
query(smokes(p85)).
evidence(cancer(p87),true).
query(smokes(p87)).
query(smokes(p88)).
query(cancer(p88)).
evidence(smokes(p89),false).
evidence(cancer(p89),false).
evidence(cancer(p9),false).
query(smokes(p9)).
evidence(smokes(p90),true).
evidence(cancer(p90),false).
query(smokes(p91)).
query(cancer(p91)).
evidence(smokes(p92),true).
query(cancer(p92)).
evidence(smokes(p93),true).
query(cancer(p93)).
evidence(cancer(p94),false).
query(smokes(p94)).
friend(p4,p61).
friend(p61,p4).
friend(p4,p28).
friend(p28,p4).
friend(p84,p94).
friend(p94,p84).
friend(p26,p38).
friend(p38,p26).
friend(p44,p47).
friend(p47,p44).
friend(p13,p14).
friend(p14,p13).
friend(p8,p14).
friend(p14,p8).
friend(p4,p13).
friend(p13,p4).
friend(p54,p55).
friend(p55,p54).
friend(p7,p14).
friend(p14,p7).
friend(p2,p55).
friend(p55,p2).
friend(p38,p84).
friend(p84,p38).
friend(p46,p52).
friend(p52,p46).
friend(p28,p36).
friend(p36,p28).
friend(p2,p49).
friend(p49,p2).
friend(p20,p55).
friend(p55,p20).
friend(p57,p84).
friend(p84,p57).
friend(p20,p37).
friend(p37,p20).
friend(p4,p24).
friend(p24,p4).
friend(p48,p55).
friend(p55,p48).
friend(p41,p61).
friend(p61,p41).
friend(p6,p75).
friend(p75,p6).
friend(p40,p70).
friend(p70,p40).
friend(p24,p28).
friend(p28,p24).
friend(p1,p25).
friend(p25,p1).
friend(p51,p54).
friend(p54,p51).
friend(p10,p77).
friend(p77,p10).
friend(p4,p10).
friend(p10,p4).
friend(p1,p49).
friend(p49,p1).
friend(p8,p49).
friend(p49,p8).
friend(p7,p13).
friend(p13,p7).
friend(p48,p60).
friend(p60,p48).
friend(p27,p71).
friend(p71,p27).
friend(p36,p76).
friend(p76,p36).
friend(p36,p48).
friend(p48,p36).
friend(p34,p53).
friend(p53,p34).
friend(p16,p19).
friend(p19,p16).
friend(p60,p66).
friend(p66,p60).
friend(p74,p77).
friend(p77,p74).
friend(p66,p92).
friend(p92,p66).
friend(p50,p83).
friend(p83,p50).
friend(p10,p59).
friend(p59,p10).
friend(p1,p2).
friend(p2,p1).
friend(p13,p42).
friend(p42,p13).
friend(p2,p3).
friend(p3,p2).
friend(p1,p48).
friend(p48,p1).
friend(p33,p45).
friend(p45,p33).
friend(p15,p26).
friend(p26,p15).
friend(p24,p55).
friend(p55,p24).
friend(p36,p61).
friend(p61,p36).
friend(p11,p18).
friend(p18,p11).
friend(p5,p88).
friend(p88,p5).
friend(p3,p6).
friend(p6,p3).
friend(p21,p55).
friend(p55,p21).
friend(p2,p5).
friend(p5,p2).
friend(p52,p54).
friend(p54,p52).
friend(p72,p76).
friend(p76,p72).
friend(p8,p60).
friend(p60,p8).
friend(p26,p28).
friend(p28,p26).
friend(p1,p24).
friend(p24,p1).
friend(p31,p55).
friend(p55,p31).
friend(p60,p64).
friend(p64,p60).
friend(p15,p21).
friend(p21,p15).
friend(p25,p68).
friend(p68,p25).
friend(p24,p46).
friend(p46,p24).
friend(p5,p13).
friend(p13,p5).
friend(p55,p56).
friend(p56,p55).
friend(p19,p20).
friend(p20,p19).
friend(p21,p61).
friend(p61,p21).
friend(p14,p50).
friend(p50,p14).
friend(p51,p81).
friend(p81,p51).
friend(p62,p68).
friend(p68,p62).
friend(p64,p65).
friend(p65,p64).
friend(p7,p54).
friend(p54,p7).
friend(p10,p34).
friend(p34,p10).
friend(p16,p44).
friend(p44,p16).
friend(p26,p73).
friend(p73,p26).
friend(p25,p45).
friend(p45,p25).
friend(p58,p84).
friend(p84,p58).
friend(p2,p9).
friend(p9,p2).
friend(p52,p61).
friend(p61,p52).
friend(p89,p92).
friend(p92,p89).
friend(p64,p69).
friend(p69,p64).
friend(p33,p34).
friend(p34,p33).
friend(p2,p71).
friend(p71,p2).
friend(p1,p7).
friend(p7,p1).
friend(p18,p63).
friend(p63,p18).
friend(p26,p79).
friend(p79,p26).
friend(p27,p28).
friend(p28,p27).
friend(p49,p55).
friend(p55,p49).
friend(p31,p58).
friend(p58,p31).
friend(p34,p58).
friend(p58,p34).
friend(p55,p67).
friend(p67,p55).
friend(p37,p40).
friend(p40,p37).
friend(p19,p66).
friend(p66,p19).
friend(p91,p93).
friend(p93,p91).
friend(p52,p58).
friend(p58,p52).
friend(p53,p76).
friend(p76,p53).
friend(p27,p51).
friend(p51,p27).
friend(p19,p38).
friend(p38,p19).
friend(p6,p15).
friend(p15,p6).
friend(p2,p24).
friend(p24,p2).
friend(p16,p87).
friend(p87,p16).
friend(p32,p46).
friend(p46,p32).
friend(p39,p43).
friend(p43,p39).
friend(p19,p90).
friend(p90,p19).
friend(p42,p72).
friend(p72,p42).
friend(p25,p81).
friend(p81,p25).
friend(p25,p32).
friend(p32,p25).
friend(p4,p5).
friend(p5,p4).
friend(p4,p21).
friend(p21,p4).
friend(p5,p51).
friend(p51,p5).
friend(p7,p19).
friend(p19,p7).
friend(p37,p72).
friend(p72,p37).
friend(p31,p71).
friend(p71,p31).
friend(p11,p47).
friend(p47,p11).
friend(p2,p14).
friend(p14,p2).
friend(p61,p64).
friend(p64,p61).
friend(p5,p71).
friend(p71,p5).
friend(p5,p52).
friend(p52,p5).
friend(p71,p74).
friend(p74,p71).
friend(p8,p58).
friend(p58,p8).
friend(p50,p54).
friend(p54,p50).
friend(p5,p6).
friend(p6,p5).
friend(p22,p33).
friend(p33,p22).
friend(p37,p85).
friend(p85,p37).
friend(p31,p43).
friend(p43,p31).
friend(p5,p23).
friend(p23,p5).
friend(p37,p78).
friend(p78,p37).
friend(p8,p55).
friend(p55,p8).
friend(p19,p45).
friend(p45,p19).
friend(p51,p52).
friend(p52,p51).
friend(p27,p48).
friend(p48,p27).
friend(p22,p60).
friend(p60,p22).
friend(p91,p94).
friend(p94,p91).
friend(p17,p64).
friend(p64,p17).
friend(p1,p27).
friend(p27,p1).
friend(p21,p68).
friend(p68,p21).
friend(p33,p46).
friend(p46,p33).
friend(p4,p71).
friend(p71,p4).
friend(p25,p52).
friend(p52,p25).
friend(p20,p21).
friend(p21,p20).
friend(p49,p61).
friend(p61,p49).
friend(p2,p20).
friend(p20,p2).
friend(p83,p87).
friend(p87,p83).
friend(p11,p24).
friend(p24,p11).
friend(p73,p83).
friend(p83,p73).
friend(p1,p45).
friend(p45,p1).
friend(p23,p33).
friend(p33,p23).
friend(p14,p63).
friend(p63,p14).
friend(p11,p81).
friend(p81,p11).
friend(p31,p45).
friend(p45,p31).
friend(p46,p93).
friend(p93,p46).
friend(p65,p83).
friend(p83,p65).
friend(p17,p39).
friend(p39,p17).
friend(p2,p72).
friend(p72,p2).
friend(p67,p84).
friend(p84,p67).
friend(p25,p31).
friend(p31,p25).
friend(p29,p74).
friend(p74,p29).
friend(p1,p4).
friend(p4,p1).
friend(p25,p75).
friend(p75,p25).
friend(p22,p41).
friend(p41,p22).
friend(p18,p61).
friend(p61,p18).
friend(p3,p49).
friend(p49,p3).
friend(p23,p58).
friend(p58,p23).
friend(p5,p40).
friend(p40,p5).