%%%% Reified Encoding
show(query(test)).
cont(0,6,0).
hold(19).
hold(36):-not hold(34),not hold(35).
hold(37):-not hold(33),not hold(34).
hold(39):-not hold(32),not hold(34).
hold(38):-not hold(31),not hold(32).
hold(40):-not hold(31),not hold(33).
cont(0,5,0).
cont(0,4,0).
hold(29):-not not_hold(29).
hold(27):-not not_hold(27).
hold(25):-not not_hold(25).
hold(23):-not not_hold(23).
hold(21):-not not_hold(21).
hold(48):-hold(37),hold(36).
hold(47):-hold(39),hold(36).
hold(46):-hold(39),hold(38).
hold(46):-hold(40),hold(37).
hold(45):-hold(36).
hold(44):-hold(37).
hold(42):-hold(39).
hold(43):-hold(38).
hold(41):-hold(40).
cont(0,3,0).
cont(0,2,0).
hold(28):-hold(29).
hold(26):-hold(27).
hold(24):-hold(25).
hold(22):-hold(23).
hold(20):-hold(21).
cont(0,5,1):-hold(29).
cont(0,4,1):-hold(27).
cont(0,3,1):-hold(25).
cont(0,2,1):-hold(23).
hold(37):-hold(48),hold(45).
hold(36):-hold(48),hold(44).
hold(52):-hold(48),hold(40).
hold(39):-hold(47),hold(45).
hold(36):-hold(47),hold(42).
hold(52):-hold(47),hold(38).
hold(52):-hold(46),hold(36).
hold(38):-hold(46),hold(42).
hold(40):-hold(46),hold(44).
hold(39):-hold(46),hold(43).
hold(37):-hold(46),hold(41).
hold(50):-hold(45),hold(42).
hold(49):-hold(45),hold(44).
hold(51):-hold(44),hold(41).
hold(53):-hold(44),hold(39).
hold(54):-hold(42),hold(37).
hold(53):-hold(43),hold(40).
hold(51):-hold(43),hold(42).
hold(54):-hold(41),hold(38).
hold(49):-hold(48).
hold(50):-hold(47).
hold(51):-hold(46).
hold(36):-hold(45).
hold(37):-hold(44).
hold(39):-hold(42).
hold(38):-hold(43).
hold(40):-hold(41).
cont(0,1,2):-hold(21),cont(0,2,1).
cont(0,2,2):-hold(23),cont(0,3,1).
cont(0,3,2):-hold(25),cont(0,4,1).
cont(0,4,2):-hold(27),cont(0,5,1).
cont(0,1,1):-hold(21).
cont(0,1,1):-cont(0,2,1).
cont(0,2,1):-cont(0,3,1).
cont(0,3,1):-cont(0,4,1).
cont(0,4,1):-cont(0,5,1).
cont(0,1,0).
cont(0,3,2):-cont(0,4,2).
cont(0,2,2):-cont(0,3,2).
cont(0,1,2):-cont(0,2,2).
hold(62):-cont(0,1,1).
hold(62):-cont(0,1,2).
hold(63):-cont(0,1,2).
hold(29):-hold(28).
hold(35):-hold(28).
hold(27):-hold(26).
hold(34):-hold(26).
hold(25):-hold(24).
hold(33):-hold(24).
hold(23):-hold(22).
hold(32):-hold(22).
hold(21):-hold(20).
hold(31):-hold(20).
hold(46):-hold(52),hold(45).
hold(40):-hold(52),hold(49).
hold(38):-hold(52),hold(50).
hold(36):-hold(52),hold(51).
hold(48):-hold(52),hold(41).
hold(47):-hold(52),hold(43).
hold(45):-hold(50),hold(39).
hold(55):-hold(50),hold(43).
hold(42):-hold(50),hold(36).
hold(54):-hold(50),hold(48).
hold(45):-hold(49),hold(37).
hold(55):-hold(49),hold(41).
hold(44):-hold(49),hold(36).
hold(53):-hold(49),hold(47).
hold(42):-hold(51),hold(38).
hold(44):-hold(51),hold(40).
hold(41):-hold(51),hold(37).
hold(43):-hold(51),hold(39).
hold(55):-hold(51),hold(45).
hold(39):-hold(53),hold(37).
hold(43):-hold(53),hold(41).
hold(47):-hold(53),hold(48).
hold(49):-hold(53),hold(50).
hold(40):-hold(53),hold(38).
hold(44):-hold(53),hold(42).
hold(37):-hold(54),hold(39).
hold(41):-hold(54),hold(43).
hold(48):-hold(54),hold(47).
hold(50):-hold(54),hold(49).
hold(38):-hold(54),hold(40).
hold(42):-hold(54),hold(44).
hold(55):-hold(52).
hold(56):-hold(52).
hold(47):-hold(50).
hold(48):-hold(49).
hold(46):-hold(51).
hold(54):-hold(53).
hold(53):-hold(54).
hold(64):-hold(62),not hold(63).
hold(50):-hold(55),hold(38).
hold(49):-hold(55),hold(40).
hold(45):-hold(55),hold(46).
hold(51):-hold(55),hold(36).
hold(43):-hold(55),hold(47).
hold(41):-hold(55),hold(48).
hold(52):-hold(55).
show(test):-hold(56).
show(place(1,5)):-hold(20).
show(place(1,4)):-hold(22).
show(place(1,3)):-hold(24).
show(place(1,2)):-hold(26).
show(place(1,1)):-hold(28).
query(show(test)).
prob(whold(60),160943).
evidence(bot,false).
bot:-not hold(64).
prob(not_hold(29)).
prob(not_hold(27)).
prob(not_hold(25)).
prob(not_hold(23)).
prob(not_hold(21)).
bot:-not not_hold(29),not hold(29).
bot:-not not_hold(27),not hold(27).
bot:-not not_hold(25),not hold(25).
bot:-not not_hold(23),not hold(23).
bot:-not not_hold(21),not hold(21).
bot:-hold(29),not_hold(29).
bot:-hold(27),not_hold(27).
bot:-hold(25),not_hold(25).
bot:-hold(23),not_hold(23).
bot:-hold(21),not_hold(21).


%%%% Probability part
prob(0). prob(0,0). % to avoid warnings

0.5 ::     hold(A) :- prob(    hold(A)).
0.5 :: not_hold(A) :- prob(not_hold(A)).

E/(E+1)  :: hold(A) :- prob(hold(A),W), E=2.71828182**(W/100000).

E/(E+1) :: whold(A) :- prob(whold(A),W), E=2.71828182**(W/100000).
bot :- prob(whold(A),W),     whold(A), not hold(A).
bot :- prob(whold(A),W), not whold(A),     hold(A).
