%%%% Reified Encoding
show(query(test)).
cont(0,6,0).
cont(1,6,0).
cont(2,6,0).
hold(33).
hold(34).
hold(35).
hold(74):-not hold(72),not hold(73).
hold(75):-not hold(71),not hold(72).
hold(77):-not hold(70),not hold(72).
hold(76):-not hold(69),not hold(70).
hold(78):-not hold(69),not hold(71).
cont(2,5,0).
cont(1,5,0).
cont(0,5,0).
cont(0,4,0).
cont(1,4,0).
cont(2,4,0).
hold(65):-not not_hold(65).
hold(63):-not not_hold(63).
hold(61):-not not_hold(61).
hold(59):-not not_hold(59).
hold(57):-not not_hold(57).
hold(55):-not not_hold(55).
hold(53):-not not_hold(53).
hold(51):-not not_hold(51).
hold(49):-not not_hold(49).
hold(47):-not not_hold(47).
hold(45):-not not_hold(45).
hold(43):-not not_hold(43).
hold(41):-not not_hold(41).
hold(39):-not not_hold(39).
hold(37):-not not_hold(37).
hold(86):-hold(75),hold(74).
hold(85):-hold(77),hold(74).
hold(84):-hold(77),hold(76).
hold(84):-hold(78),hold(75).
hold(83):-hold(74).
hold(82):-hold(75).
hold(80):-hold(77).
hold(81):-hold(76).
hold(79):-hold(78).
cont(2,3,0).
cont(1,3,0).
cont(0,3,0).
cont(0,2,0).
cont(1,2,0).
cont(2,2,0).
hold(64):-hold(65).
hold(62):-hold(63).
hold(60):-hold(61).
hold(58):-hold(59).
hold(56):-hold(57).
hold(54):-hold(55).
hold(52):-hold(53).
hold(50):-hold(51).
hold(48):-hold(49).
hold(46):-hold(47).
hold(44):-hold(45).
hold(42):-hold(43).
hold(40):-hold(41).
hold(38):-hold(39).
hold(36):-hold(37).
cont(0,5,1):-hold(65).
cont(0,4,1):-hold(63).
cont(0,3,1):-hold(61).
cont(0,2,1):-hold(59).
cont(1,5,1):-hold(55).
cont(1,4,1):-hold(53).
cont(1,3,1):-hold(51).
cont(1,2,1):-hold(49).
cont(2,5,1):-hold(45).
cont(2,4,1):-hold(43).
cont(2,3,1):-hold(41).
cont(2,2,1):-hold(39).
hold(75):-hold(86),hold(83).
hold(74):-hold(86),hold(82).
hold(90):-hold(86),hold(78).
hold(77):-hold(85),hold(83).
hold(74):-hold(85),hold(80).
hold(90):-hold(85),hold(76).
hold(90):-hold(84),hold(74).
hold(76):-hold(84),hold(80).
hold(78):-hold(84),hold(82).
hold(77):-hold(84),hold(81).
hold(75):-hold(84),hold(79).
hold(88):-hold(83),hold(80).
hold(87):-hold(83),hold(82).
hold(89):-hold(82),hold(79).
hold(91):-hold(82),hold(77).
hold(92):-hold(80),hold(75).
hold(91):-hold(81),hold(78).
hold(89):-hold(81),hold(80).
hold(92):-hold(79),hold(76).
hold(87):-hold(86).
hold(88):-hold(85).
hold(89):-hold(84).
hold(74):-hold(83).
hold(75):-hold(82).
hold(77):-hold(80).
hold(76):-hold(81).
hold(78):-hold(79).
cont(2,1,2):-hold(37),cont(2,2,1).
cont(2,2,2):-hold(39),cont(2,3,1).
cont(2,3,2):-hold(41),cont(2,4,1).
cont(2,4,2):-hold(43),cont(2,5,1).
cont(1,1,2):-hold(47),cont(1,2,1).
cont(1,2,2):-hold(49),cont(1,3,1).
cont(1,3,2):-hold(51),cont(1,4,1).
cont(1,4,2):-hold(53),cont(1,5,1).
cont(0,1,2):-hold(57),cont(0,2,1).
cont(0,2,2):-hold(59),cont(0,3,1).
cont(0,3,2):-hold(61),cont(0,4,1).
cont(0,4,2):-hold(63),cont(0,5,1).
cont(2,1,1):-hold(37).
cont(1,1,1):-hold(47).
cont(0,1,1):-hold(57).
cont(2,1,1):-cont(2,2,1).
cont(2,2,1):-cont(2,3,1).
cont(2,3,1):-cont(2,4,1).
cont(2,4,1):-cont(2,5,1).
cont(1,1,1):-cont(1,2,1).
cont(1,2,1):-cont(1,3,1).
cont(1,3,1):-cont(1,4,1).
cont(1,4,1):-cont(1,5,1).
cont(0,1,1):-cont(0,2,1).
cont(0,2,1):-cont(0,3,1).
cont(0,3,1):-cont(0,4,1).
cont(0,4,1):-cont(0,5,1).
cont(2,1,0).
cont(1,1,0).
cont(0,1,0).
cont(0,3,2):-cont(0,4,2).
cont(0,2,2):-cont(0,3,2).
cont(0,1,2):-cont(0,2,2).
cont(1,3,2):-cont(1,4,2).
cont(1,2,2):-cont(1,3,2).
cont(1,1,2):-cont(1,2,2).
cont(2,3,2):-cont(2,4,2).
cont(2,2,2):-cont(2,3,2).
cont(2,1,2):-cont(2,2,2).
hold(108):-cont(0,1,1).
hold(111):-cont(1,1,1).
hold(114):-cont(2,1,1).
hold(108):-cont(0,1,2).
hold(109):-cont(0,1,2).
hold(111):-cont(1,1,2).
hold(112):-cont(1,1,2).
hold(114):-cont(2,1,2).
hold(115):-cont(2,1,2).
hold(65):-hold(64).
hold(73):-hold(64).
hold(63):-hold(62).
hold(72):-hold(62).
hold(61):-hold(60).
hold(71):-hold(60).
hold(59):-hold(58).
hold(70):-hold(58).
hold(57):-hold(56).
hold(69):-hold(56).
hold(55):-hold(54).
hold(73):-hold(54).
hold(53):-hold(52).
hold(72):-hold(52).
hold(51):-hold(50).
hold(71):-hold(50).
hold(49):-hold(48).
hold(70):-hold(48).
hold(47):-hold(46).
hold(69):-hold(46).
hold(45):-hold(44).
hold(73):-hold(44).
hold(43):-hold(42).
hold(72):-hold(42).
hold(41):-hold(40).
hold(71):-hold(40).
hold(39):-hold(38).
hold(70):-hold(38).
hold(37):-hold(36).
hold(69):-hold(36).
hold(84):-hold(90),hold(83).
hold(78):-hold(90),hold(87).
hold(76):-hold(90),hold(88).
hold(74):-hold(90),hold(89).
hold(86):-hold(90),hold(79).
hold(85):-hold(90),hold(81).
hold(83):-hold(88),hold(77).
hold(93):-hold(88),hold(81).
hold(80):-hold(88),hold(74).
hold(92):-hold(88),hold(86).
hold(83):-hold(87),hold(75).
hold(93):-hold(87),hold(79).
hold(82):-hold(87),hold(74).
hold(91):-hold(87),hold(85).
hold(80):-hold(89),hold(76).
hold(82):-hold(89),hold(78).
hold(79):-hold(89),hold(75).
hold(81):-hold(89),hold(77).
hold(93):-hold(89),hold(83).
hold(77):-hold(91),hold(75).
hold(81):-hold(91),hold(79).
hold(85):-hold(91),hold(86).
hold(87):-hold(91),hold(88).
hold(78):-hold(91),hold(76).
hold(82):-hold(91),hold(80).
hold(75):-hold(92),hold(77).
hold(79):-hold(92),hold(81).
hold(86):-hold(92),hold(85).
hold(88):-hold(92),hold(87).
hold(76):-hold(92),hold(78).
hold(80):-hold(92),hold(82).
hold(93):-hold(90).
hold(94):-hold(90).
hold(85):-hold(88).
hold(86):-hold(87).
hold(84):-hold(89).
hold(92):-hold(91).
hold(91):-hold(92).
hold(110):-hold(108),not hold(109).
hold(113):-hold(111),not hold(112).
hold(116):-hold(114),not hold(115).
hold(88):-hold(93),hold(76).
hold(87):-hold(93),hold(78).
hold(83):-hold(93),hold(84).
hold(89):-hold(93),hold(74).
hold(81):-hold(93),hold(85).
hold(79):-hold(93),hold(86).
hold(90):-hold(93).
show(place(1,1)):-hold(64).
show(place(1,2)):-hold(62).
show(place(1,3)):-hold(60).
show(place(1,4)):-hold(58).
show(place(1,5)):-hold(56).
show(place(2,1)):-hold(54).
show(place(2,2)):-hold(52).
show(place(2,3)):-hold(50).
show(place(2,4)):-hold(48).
show(place(2,5)):-hold(46).
show(place(3,1)):-hold(44).
show(place(3,2)):-hold(42).
show(place(3,3)):-hold(40).
show(place(3,4)):-hold(38).
show(place(3,5)):-hold(36).
show(test):-hold(94).
query(show(test)).
prob(whold(104),160943).
evidence(bot,false).
bot:-hold(46),hold(36).
bot:-hold(48),hold(36).
bot:-hold(50),hold(36).
bot:-hold(52),hold(36).
bot:-hold(54),hold(36).
bot:-hold(56),hold(36).
bot:-hold(58),hold(36).
bot:-hold(60),hold(36).
bot:-hold(62),hold(36).
bot:-hold(64),hold(36).
bot:-hold(48),hold(38).
bot:-hold(50),hold(38).
bot:-hold(52),hold(38).
bot:-hold(54),hold(38).
bot:-hold(58),hold(38).
bot:-hold(60),hold(38).
bot:-hold(62),hold(38).
bot:-hold(64),hold(38).
bot:-hold(50),hold(40).
bot:-hold(52),hold(40).
bot:-hold(54),hold(40).
bot:-hold(60),hold(40).
bot:-hold(62),hold(40).
bot:-hold(64),hold(40).
bot:-hold(52),hold(42).
bot:-hold(54),hold(42).
bot:-hold(62),hold(42).
bot:-hold(64),hold(42).
bot:-hold(54),hold(44).
bot:-hold(64),hold(44).
bot:-hold(56),hold(46).
bot:-hold(58),hold(46).
bot:-hold(60),hold(46).
bot:-hold(62),hold(46).
bot:-hold(64),hold(46).
bot:-hold(58),hold(48).
bot:-hold(60),hold(48).
bot:-hold(62),hold(48).
bot:-hold(64),hold(48).
bot:-hold(60),hold(50).
bot:-hold(62),hold(50).
bot:-hold(64),hold(50).
bot:-hold(62),hold(52).
bot:-hold(64),hold(52).
bot:-hold(64),hold(54).
bot:-not hold(110).
bot:-not hold(113).
bot:-not hold(116).
prob(not_hold(65)).
prob(not_hold(63)).
prob(not_hold(61)).
prob(not_hold(59)).
prob(not_hold(57)).
prob(not_hold(55)).
prob(not_hold(53)).
prob(not_hold(51)).
prob(not_hold(49)).
prob(not_hold(47)).
prob(not_hold(45)).
prob(not_hold(43)).
prob(not_hold(41)).
prob(not_hold(39)).
prob(not_hold(37)).
bot:-not not_hold(65),not hold(65).
bot:-not not_hold(63),not hold(63).
bot:-not not_hold(61),not hold(61).
bot:-not not_hold(59),not hold(59).
bot:-not not_hold(57),not hold(57).
bot:-not not_hold(55),not hold(55).
bot:-not not_hold(53),not hold(53).
bot:-not not_hold(51),not hold(51).
bot:-not not_hold(49),not hold(49).
bot:-not not_hold(47),not hold(47).
bot:-not not_hold(45),not hold(45).
bot:-not not_hold(43),not hold(43).
bot:-not not_hold(41),not hold(41).
bot:-not not_hold(39),not hold(39).
bot:-not not_hold(37),not hold(37).
bot:-hold(65),not_hold(65).
bot:-hold(63),not_hold(63).
bot:-hold(61),not_hold(61).
bot:-hold(59),not_hold(59).
bot:-hold(57),not_hold(57).
bot:-hold(55),not_hold(55).
bot:-hold(53),not_hold(53).
bot:-hold(51),not_hold(51).
bot:-hold(49),not_hold(49).
bot:-hold(47),not_hold(47).
bot:-hold(45),not_hold(45).
bot:-hold(43),not_hold(43).
bot:-hold(41),not_hold(41).
bot:-hold(39),not_hold(39).
bot:-hold(37),not_hold(37).


%%%% Probability part
prob(0). prob(0,0). % to avoid warnings

0.5 ::     hold(A) :- prob(    hold(A)).
0.5 :: not_hold(A) :- prob(not_hold(A)).

E/(E+1)  :: hold(A) :- prob(hold(A),W), E=2.71828182**(W/100000).

E/(E+1) :: whold(A) :- prob(whold(A),W), E=2.71828182**(W/100000).
bot :- prob(whold(A),W),     whold(A), not hold(A).
bot :- prob(whold(A),W), not whold(A),     hold(A).
