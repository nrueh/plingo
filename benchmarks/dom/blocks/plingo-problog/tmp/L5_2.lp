%%%% Reified Encoding
show(query(test)).
cont(0,6,0).
cont(1,6,0).
hold(26).
hold(27).
hold(55):-not hold(53),not hold(54).
hold(56):-not hold(52),not hold(53).
hold(58):-not hold(51),not hold(53).
hold(57):-not hold(50),not hold(51).
hold(59):-not hold(50),not hold(52).
cont(1,5,0).
cont(0,5,0).
cont(0,4,0).
cont(1,4,0).
hold(47):-not not_hold(47).
hold(45):-not not_hold(45).
hold(43):-not not_hold(43).
hold(41):-not not_hold(41).
hold(39):-not not_hold(39).
hold(37):-not not_hold(37).
hold(35):-not not_hold(35).
hold(33):-not not_hold(33).
hold(31):-not not_hold(31).
hold(29):-not not_hold(29).
hold(67):-hold(56),hold(55).
hold(66):-hold(58),hold(55).
hold(65):-hold(58),hold(57).
hold(65):-hold(59),hold(56).
hold(64):-hold(55).
hold(63):-hold(56).
hold(61):-hold(58).
hold(62):-hold(57).
hold(60):-hold(59).
cont(1,3,0).
cont(0,3,0).
cont(0,2,0).
cont(1,2,0).
hold(46):-hold(47).
hold(44):-hold(45).
hold(42):-hold(43).
hold(40):-hold(41).
hold(38):-hold(39).
hold(36):-hold(37).
hold(34):-hold(35).
hold(32):-hold(33).
hold(30):-hold(31).
hold(28):-hold(29).
cont(0,5,1):-hold(47).
cont(0,4,1):-hold(45).
cont(0,3,1):-hold(43).
cont(0,2,1):-hold(41).
cont(1,5,1):-hold(37).
cont(1,4,1):-hold(35).
cont(1,3,1):-hold(33).
cont(1,2,1):-hold(31).
hold(56):-hold(67),hold(64).
hold(55):-hold(67),hold(63).
hold(71):-hold(67),hold(59).
hold(58):-hold(66),hold(64).
hold(55):-hold(66),hold(61).
hold(71):-hold(66),hold(57).
hold(71):-hold(65),hold(55).
hold(57):-hold(65),hold(61).
hold(59):-hold(65),hold(63).
hold(58):-hold(65),hold(62).
hold(56):-hold(65),hold(60).
hold(69):-hold(64),hold(61).
hold(68):-hold(64),hold(63).
hold(70):-hold(63),hold(60).
hold(72):-hold(63),hold(58).
hold(73):-hold(61),hold(56).
hold(72):-hold(62),hold(59).
hold(70):-hold(62),hold(61).
hold(73):-hold(60),hold(57).
hold(68):-hold(67).
hold(69):-hold(66).
hold(70):-hold(65).
hold(55):-hold(64).
hold(56):-hold(63).
hold(58):-hold(61).
hold(57):-hold(62).
hold(59):-hold(60).
cont(1,1,2):-hold(29),cont(1,2,1).
cont(1,2,2):-hold(31),cont(1,3,1).
cont(1,3,2):-hold(33),cont(1,4,1).
cont(1,4,2):-hold(35),cont(1,5,1).
cont(0,1,2):-hold(39),cont(0,2,1).
cont(0,2,2):-hold(41),cont(0,3,1).
cont(0,3,2):-hold(43),cont(0,4,1).
cont(0,4,2):-hold(45),cont(0,5,1).
cont(1,1,1):-hold(29).
cont(0,1,1):-hold(39).
cont(1,1,1):-cont(1,2,1).
cont(1,2,1):-cont(1,3,1).
cont(1,3,1):-cont(1,4,1).
cont(1,4,1):-cont(1,5,1).
cont(0,1,1):-cont(0,2,1).
cont(0,2,1):-cont(0,3,1).
cont(0,3,1):-cont(0,4,1).
cont(0,4,1):-cont(0,5,1).
cont(1,1,0).
cont(0,1,0).
cont(0,3,2):-cont(0,4,2).
cont(0,2,2):-cont(0,3,2).
cont(0,1,2):-cont(0,2,2).
cont(1,3,2):-cont(1,4,2).
cont(1,2,2):-cont(1,3,2).
cont(1,1,2):-cont(1,2,2).
hold(85):-cont(0,1,1).
hold(88):-cont(1,1,1).
hold(85):-cont(0,1,2).
hold(86):-cont(0,1,2).
hold(88):-cont(1,1,2).
hold(89):-cont(1,1,2).
hold(47):-hold(46).
hold(54):-hold(46).
hold(45):-hold(44).
hold(53):-hold(44).
hold(43):-hold(42).
hold(52):-hold(42).
hold(41):-hold(40).
hold(51):-hold(40).
hold(39):-hold(38).
hold(50):-hold(38).
hold(37):-hold(36).
hold(54):-hold(36).
hold(35):-hold(34).
hold(53):-hold(34).
hold(33):-hold(32).
hold(52):-hold(32).
hold(31):-hold(30).
hold(51):-hold(30).
hold(29):-hold(28).
hold(50):-hold(28).
hold(65):-hold(71),hold(64).
hold(59):-hold(71),hold(68).
hold(57):-hold(71),hold(69).
hold(55):-hold(71),hold(70).
hold(67):-hold(71),hold(60).
hold(66):-hold(71),hold(62).
hold(64):-hold(69),hold(58).
hold(74):-hold(69),hold(62).
hold(61):-hold(69),hold(55).
hold(73):-hold(69),hold(67).
hold(64):-hold(68),hold(56).
hold(74):-hold(68),hold(60).
hold(63):-hold(68),hold(55).
hold(72):-hold(68),hold(66).
hold(61):-hold(70),hold(57).
hold(63):-hold(70),hold(59).
hold(60):-hold(70),hold(56).
hold(62):-hold(70),hold(58).
hold(74):-hold(70),hold(64).
hold(58):-hold(72),hold(56).
hold(62):-hold(72),hold(60).
hold(66):-hold(72),hold(67).
hold(68):-hold(72),hold(69).
hold(59):-hold(72),hold(57).
hold(63):-hold(72),hold(61).
hold(56):-hold(73),hold(58).
hold(60):-hold(73),hold(62).
hold(67):-hold(73),hold(66).
hold(69):-hold(73),hold(68).
hold(57):-hold(73),hold(59).
hold(61):-hold(73),hold(63).
hold(74):-hold(71).
hold(75):-hold(71).
hold(66):-hold(69).
hold(67):-hold(68).
hold(65):-hold(70).
hold(73):-hold(72).
hold(72):-hold(73).
hold(87):-hold(85),not hold(86).
hold(90):-hold(88),not hold(89).
hold(69):-hold(74),hold(57).
hold(68):-hold(74),hold(59).
hold(64):-hold(74),hold(65).
hold(70):-hold(74),hold(55).
hold(62):-hold(74),hold(66).
hold(60):-hold(74),hold(67).
hold(71):-hold(74).
show(place(1,1)):-hold(46).
show(place(1,2)):-hold(44).
show(place(1,3)):-hold(42).
show(place(1,4)):-hold(40).
show(place(1,5)):-hold(38).
show(place(2,1)):-hold(36).
show(place(2,2)):-hold(34).
show(place(2,3)):-hold(32).
show(place(2,4)):-hold(30).
show(place(2,5)):-hold(28).
show(test):-hold(75).
query(show(test)).
prob(whold(82),160943).
evidence(bot,false).
bot:-hold(38),hold(28).
bot:-hold(40),hold(28).
bot:-hold(42),hold(28).
bot:-hold(44),hold(28).
bot:-hold(46),hold(28).
bot:-hold(40),hold(30).
bot:-hold(42),hold(30).
bot:-hold(44),hold(30).
bot:-hold(46),hold(30).
bot:-hold(42),hold(32).
bot:-hold(44),hold(32).
bot:-hold(46),hold(32).
bot:-hold(44),hold(34).
bot:-hold(46),hold(34).
bot:-hold(46),hold(36).
bot:-not hold(87).
bot:-not hold(90).
prob(not_hold(47)).
prob(not_hold(45)).
prob(not_hold(43)).
prob(not_hold(41)).
prob(not_hold(39)).
prob(not_hold(37)).
prob(not_hold(35)).
prob(not_hold(33)).
prob(not_hold(31)).
prob(not_hold(29)).
bot:-not not_hold(47),not hold(47).
bot:-not not_hold(45),not hold(45).
bot:-not not_hold(43),not hold(43).
bot:-not not_hold(41),not hold(41).
bot:-not not_hold(39),not hold(39).
bot:-not not_hold(37),not hold(37).
bot:-not not_hold(35),not hold(35).
bot:-not not_hold(33),not hold(33).
bot:-not not_hold(31),not hold(31).
bot:-not not_hold(29),not hold(29).
bot:-hold(47),not_hold(47).
bot:-hold(45),not_hold(45).
bot:-hold(43),not_hold(43).
bot:-hold(41),not_hold(41).
bot:-hold(39),not_hold(39).
bot:-hold(37),not_hold(37).
bot:-hold(35),not_hold(35).
bot:-hold(33),not_hold(33).
bot:-hold(31),not_hold(31).
bot:-hold(29),not_hold(29).


%%%% Probability part
prob(0). prob(0,0). % to avoid warnings

0.5 ::     hold(A) :- prob(    hold(A)).
0.5 :: not_hold(A) :- prob(not_hold(A)).

E/(E+1)  :: hold(A) :- prob(hold(A),W), E=2.71828182**(W/100000).

E/(E+1) :: whold(A) :- prob(whold(A),W), E=2.71828182**(W/100000).
bot :- prob(whold(A),W),     whold(A), not hold(A).
bot :- prob(whold(A),W), not whold(A),     hold(A).
