:- ['kb_smokes'].
people([p1,p10,p100,p11,p12,p13,p14,p15,p16,p17,p18,p19,p2,p20,p21,p22,p24,p26,p27,p28,p29,p3,p30,p31,p32,p33,p34,p35,p36,p37,p38,p39,p4,p40,p41,p42,p43,p45,p46,p47,p48,p49,p5,p51,p52,p53,p54,p55,p56,p57,p58,p59,p6,p60,p61,p62,p63,p64,p65,p66,p69,p7,p71,p72,p73,p75,p76,p77,p78,p79,p8,p80,p81,p82,p83,p84,p85,p86,p87,p88,p89,p9,p90,p91,p94,p95,p96,p97,p98,p99]).
evidence(cancer(p1),false).
query(smokes(p1)).
query(smokes(p10)).
query(cancer(p10)).
evidence(smokes(p100),false).
evidence(cancer(p100),false).
evidence(smokes(p11),false).
evidence(cancer(p11),false).
evidence(smokes(p12),false).
query(cancer(p12)).
evidence(cancer(p13),false).
query(smokes(p13)).
query(smokes(p14)).
query(cancer(p14)).
evidence(smokes(p15),false).
query(cancer(p15)).
evidence(smokes(p16),true).
evidence(cancer(p16),false).
evidence(smokes(p17),false).
query(cancer(p17)).
evidence(cancer(p18),false).
query(smokes(p18)).
evidence(smokes(p19),false).
evidence(cancer(p19),true).
evidence(cancer(p2),false).
query(smokes(p2)).
evidence(cancer(p20),false).
query(smokes(p20)).
query(smokes(p21)).
query(cancer(p21)).
evidence(cancer(p22),true).
query(smokes(p22)).
evidence(smokes(p24),true).
query(cancer(p24)).
evidence(cancer(p26),false).
query(smokes(p26)).
evidence(smokes(p27),false).
evidence(cancer(p27),false).
evidence(smokes(p28),true).
query(cancer(p28)).
evidence(smokes(p29),true).
evidence(cancer(p29),false).
query(smokes(p3)).
query(cancer(p3)).
evidence(cancer(p30),false).
query(smokes(p30)).
evidence(smokes(p31),false).
evidence(cancer(p31),true).
evidence(cancer(p32),true).
query(smokes(p32)).
evidence(cancer(p33),false).
query(smokes(p33)).
evidence(smokes(p34),false).
query(cancer(p34)).
query(smokes(p35)).
query(cancer(p35)).
evidence(smokes(p36),true).
evidence(cancer(p36),false).
evidence(cancer(p37),false).
query(smokes(p37)).
query(smokes(p38)).
query(cancer(p38)).
evidence(smokes(p39),false).
evidence(cancer(p39),false).
query(smokes(p4)).
query(cancer(p4)).
query(smokes(p40)).
query(cancer(p40)).
evidence(smokes(p41),true).
evidence(cancer(p41),false).
query(smokes(p42)).
query(cancer(p42)).
evidence(smokes(p43),true).
evidence(cancer(p43),false).
evidence(cancer(p45),false).
query(smokes(p45)).
query(smokes(p46)).
query(cancer(p46)).
evidence(cancer(p47),false).
query(smokes(p47)).
evidence(smokes(p48),false).
query(cancer(p48)).
evidence(cancer(p49),true).
query(smokes(p49)).
evidence(cancer(p5),false).
query(smokes(p5)).
query(smokes(p51)).
query(cancer(p51)).
evidence(cancer(p52),true).
query(smokes(p52)).
evidence(smokes(p53),true).
evidence(cancer(p53),true).
evidence(smokes(p54),false).
query(cancer(p54)).
evidence(smokes(p55),false).
evidence(cancer(p55),false).
evidence(smokes(p56),true).
query(cancer(p56)).
evidence(smokes(p57),true).
query(cancer(p57)).
evidence(cancer(p58),false).
query(smokes(p58)).
evidence(smokes(p59),false).
query(cancer(p59)).
evidence(smokes(p6),false).
evidence(cancer(p6),false).
query(smokes(p60)).
query(cancer(p60)).
evidence(smokes(p61),true).
query(cancer(p61)).
evidence(cancer(p62),false).
query(smokes(p62)).
evidence(smokes(p63),false).
query(cancer(p63)).
evidence(cancer(p64),false).
query(smokes(p64)).
query(smokes(p65)).
query(cancer(p65)).
query(smokes(p66)).
query(cancer(p66)).
evidence(smokes(p69),false).
query(cancer(p69)).
evidence(cancer(p7),true).
query(smokes(p7)).
evidence(cancer(p71),false).
query(smokes(p71)).
evidence(smokes(p72),false).
query(cancer(p72)).
evidence(smokes(p73),true).
evidence(cancer(p73),false).
evidence(smokes(p75),true).
evidence(cancer(p75),true).
evidence(smokes(p76),true).
query(cancer(p76)).
evidence(cancer(p77),false).
query(smokes(p77)).
evidence(cancer(p78),false).
query(smokes(p78)).
query(smokes(p79)).
query(cancer(p79)).
evidence(cancer(p8),false).
query(smokes(p8)).
evidence(cancer(p80),true).
query(smokes(p80)).
evidence(smokes(p81),true).
evidence(cancer(p81),true).
evidence(cancer(p82),false).
query(smokes(p82)).
evidence(cancer(p83),false).
query(smokes(p83)).
evidence(cancer(p84),false).
query(smokes(p84)).
evidence(smokes(p85),false).
query(cancer(p85)).
query(smokes(p86)).
query(cancer(p86)).
evidence(cancer(p87),false).
query(smokes(p87)).
query(smokes(p88)).
query(cancer(p88)).
query(smokes(p89)).
query(cancer(p89)).
evidence(smokes(p9),false).
evidence(cancer(p9),false).
evidence(smokes(p90),false).
evidence(cancer(p90),false).
evidence(smokes(p91),true).
query(cancer(p91)).
evidence(smokes(p94),true).
evidence(cancer(p94),true).
evidence(smokes(p95),false).
evidence(cancer(p95),false).
evidence(smokes(p96),false).
evidence(cancer(p96),false).
evidence(smokes(p97),false).
evidence(cancer(p97),false).
evidence(smokes(p98),false).
evidence(cancer(p98),false).
evidence(smokes(p99),false).
query(cancer(p99)).
friend(p56,p79).
friend(p79,p56).
friend(p14,p35).
friend(p35,p14).
friend(p15,p42).
friend(p42,p15).
friend(p54,p79).
friend(p79,p54).
friend(p2,p27).
friend(p27,p2).
friend(p66,p99).
friend(p99,p66).
friend(p7,p29).
friend(p29,p7).
friend(p40,p59).
friend(p59,p40).
friend(p7,p76).
friend(p76,p7).
friend(p13,p19).
friend(p19,p13).
friend(p53,p57).
friend(p57,p53).
friend(p43,p81).
friend(p81,p43).
friend(p4,p17).
friend(p17,p4).
friend(p51,p60).
friend(p60,p51).
friend(p26,p39).
friend(p39,p26).
friend(p26,p38).
friend(p38,p26).
friend(p19,p29).
friend(p29,p19).
friend(p21,p46).
friend(p46,p21).
friend(p10,p75).
friend(p75,p10).
friend(p11,p48).
friend(p48,p11).
friend(p96,p97).
friend(p97,p96).
friend(p71,p82).
friend(p82,p71).
friend(p36,p57).
friend(p57,p36).
friend(p16,p22).
friend(p22,p16).
friend(p5,p42).
friend(p42,p5).
friend(p57,p73).
friend(p73,p57).
friend(p71,p76).
friend(p76,p71).
friend(p29,p33).
friend(p33,p29).
friend(p54,p89).
friend(p89,p54).
friend(p6,p10).
friend(p10,p6).
friend(p63,p72).
friend(p72,p63).
friend(p3,p53).
friend(p53,p3).
friend(p41,p43).
friend(p43,p41).
friend(p17,p98).
friend(p98,p17).
friend(p88,p100).
friend(p100,p88).
friend(p54,p58).
friend(p58,p54).
friend(p40,p90).
friend(p90,p40).
friend(p90,p96).
friend(p96,p90).
friend(p14,p18).
friend(p18,p14).
friend(p12,p84).
friend(p84,p12).
friend(p10,p38).
friend(p38,p10).
friend(p5,p17).
friend(p17,p5).
friend(p4,p7).
friend(p7,p4).
friend(p26,p29).
friend(p29,p26).
friend(p4,p10).
friend(p10,p4).
friend(p27,p88).
friend(p88,p27).
friend(p21,p54).
friend(p54,p21).
friend(p29,p79).
friend(p79,p29).
friend(p12,p35).
friend(p35,p12).
friend(p64,p91).
friend(p91,p64).
friend(p9,p34).
friend(p34,p9).
friend(p16,p91).
friend(p91,p16).
friend(p20,p45).
friend(p45,p20).
friend(p35,p59).
friend(p59,p35).
friend(p16,p19).
friend(p19,p16).
friend(p48,p79).
friend(p79,p48).
friend(p4,p11).
friend(p11,p4).
friend(p8,p47).
friend(p47,p8).
friend(p29,p94).
friend(p94,p29).
friend(p63,p88).
friend(p88,p63).
friend(p1,p32).
friend(p32,p1).
friend(p12,p62).
friend(p62,p12).
friend(p1,p2).
friend(p2,p1).
friend(p4,p22).
friend(p22,p4).
friend(p1,p51).
friend(p51,p1).
friend(p9,p54).
friend(p54,p9).
friend(p4,p14).
friend(p14,p4).
friend(p3,p57).
friend(p57,p3).
friend(p82,p88).
friend(p88,p82).
friend(p2,p3).
friend(p3,p2).
friend(p13,p26).
friend(p26,p13).
friend(p91,p100).
friend(p100,p91).
friend(p1,p26).
friend(p26,p1).
friend(p29,p43).
friend(p43,p29).
friend(p59,p71).
friend(p71,p59).
friend(p15,p38).
friend(p38,p15).
friend(p60,p83).
friend(p83,p60).
friend(p3,p6).
friend(p6,p3).
friend(p39,p41).
friend(p41,p39).
friend(p21,p24).
friend(p24,p21).
friend(p8,p10).
friend(p10,p8).
friend(p63,p87).
friend(p87,p63).
friend(p66,p69).
friend(p69,p66).
friend(p30,p37).
friend(p37,p30).
friend(p6,p49).
friend(p49,p6).
friend(p21,p35).
friend(p35,p21).
friend(p57,p63).
friend(p63,p57).
friend(p18,p19).
friend(p19,p18).
friend(p7,p51).
friend(p51,p7).
friend(p52,p55).
friend(p55,p52).
friend(p24,p57).
friend(p57,p24).
friend(p16,p40).
friend(p40,p16).
friend(p4,p66).
friend(p66,p4).
friend(p5,p55).
friend(p55,p5).
friend(p58,p59).
friend(p59,p58).
friend(p22,p24).
friend(p24,p22).
friend(p55,p97).
friend(p97,p55).
friend(p12,p60).
friend(p60,p12).
friend(p16,p17).
friend(p17,p16).
friend(p24,p43).
friend(p43,p24).
friend(p54,p56).
friend(p56,p54).
friend(p16,p29).
friend(p29,p16).
friend(p54,p63).
friend(p63,p54).
friend(p28,p81).
friend(p81,p28).
friend(p10,p55).
friend(p55,p10).
friend(p72,p75).
friend(p75,p72).
friend(p53,p64).
friend(p64,p53).
friend(p58,p84).
friend(p84,p58).
friend(p32,p37).
friend(p37,p32).
friend(p30,p77).
friend(p77,p30).
friend(p7,p32).
friend(p32,p7).
friend(p52,p95).
friend(p95,p52).
friend(p14,p41).
friend(p41,p14).
friend(p60,p72).
friend(p72,p60).
friend(p35,p38).
friend(p38,p35).
friend(p10,p37).
friend(p37,p10).
friend(p3,p8).
friend(p8,p3).
friend(p34,p46).
friend(p46,p34).
friend(p3,p13).
friend(p13,p3).
friend(p51,p55).
friend(p55,p51).
friend(p30,p55).
friend(p55,p30).
friend(p38,p91).
friend(p91,p38).
friend(p45,p97).
friend(p97,p45).
friend(p79,p85).
friend(p85,p79).
friend(p12,p59).
friend(p59,p12).
friend(p14,p21).
friend(p21,p14).
friend(p58,p69).
friend(p69,p58).
friend(p58,p77).
friend(p77,p58).
friend(p13,p65).
friend(p65,p13).
friend(p11,p31).
friend(p31,p11).
friend(p1,p8).
friend(p8,p1).
friend(p19,p22).
friend(p22,p19).
friend(p3,p78).
friend(p78,p3).
friend(p29,p31).
friend(p31,p29).
friend(p65,p88).
friend(p88,p65).
friend(p42,p48).
friend(p48,p42).
friend(p13,p89).
friend(p89,p13).
friend(p13,p15).
friend(p15,p13).
friend(p33,p58).
friend(p58,p33).
friend(p53,p56).
friend(p56,p53).
friend(p6,p65).
friend(p65,p6).
friend(p60,p79).
friend(p79,p60).
friend(p2,p39).
friend(p39,p2).
friend(p2,p14).
friend(p14,p2).
friend(p4,p54).
friend(p54,p4).
friend(p58,p61).
friend(p61,p58).
friend(p82,p94).
friend(p94,p82).
friend(p1,p79).
friend(p79,p1).
friend(p6,p18).
friend(p18,p6).
friend(p8,p55).
friend(p55,p8).
friend(p6,p63).
friend(p63,p6).
friend(p7,p47).
friend(p47,p7).
friend(p15,p18).
friend(p18,p15).
friend(p63,p75).
friend(p75,p63).
friend(p12,p18).
friend(p18,p12).
friend(p77,p80).
friend(p80,p77).
friend(p4,p29).
friend(p29,p4).
friend(p61,p72).
friend(p72,p61).
friend(p55,p73).
friend(p73,p55).
friend(p77,p79).
friend(p79,p77).
friend(p1,p90).
friend(p90,p1).
friend(p14,p22).
friend(p22,p14).
friend(p20,p47).
friend(p47,p20).
friend(p8,p22).
friend(p22,p8).
friend(p89,p94).
friend(p94,p89).
friend(p11,p86).
friend(p86,p11).
friend(p4,p16).
friend(p16,p4).
friend(p2,p13).
friend(p13,p2).
friend(p78,p85).
friend(p85,p78).
friend(p52,p64).
friend(p64,p52).
friend(p56,p62).
friend(p62,p56).
friend(p39,p42).
friend(p42,p39).
friend(p35,p47).
friend(p47,p35).
friend(p51,p78).
friend(p78,p51).
friend(p29,p30).
friend(p30,p29).
friend(p28,p41).
friend(p41,p28).
friend(p4,p8).
friend(p8,p4).
friend(p40,p97).
friend(p97,p40).