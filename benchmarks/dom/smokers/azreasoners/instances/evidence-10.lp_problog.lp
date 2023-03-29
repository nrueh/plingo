%%%% Reified Encoding
show(query(query)).
hold(94):-hold(91),not hold(91).
hold(98):-hold(91),not hold(83).
hold(95):-hold(92),not hold(93).
hold(99):-hold(92),not hold(88).
hold(96):-hold(93),not hold(91).
hold(97):-hold(93),not hold(92).
hold(100):-hold(93),not hold(90).
query(show(query)).
prob(hold(91),138629).
prob(hold(93),138629).
prob(hold(92),138629).
prob(hold(81),109861).
prob(hold(82),109861).
prob(hold(84),109861).
prob(hold(85),109861).
prob(hold(86),109861).
prob(hold(87),109861).
prob(hold(89),109861).
prob(whold(94),-138629).
prob(whold(95),-138629).
prob(whold(96),-138629).
prob(whold(97),-138629).
prob(whold(98),-109861).
prob(whold(99),-109861).
prob(whold(100),-109861).
evidence(bot,false).
prob(hold(83)).
prob(hold(88)).
prob(hold(90)).


%%%% Probability part
prob(0). prob(0,0). % to avoid warnings

0.5 ::     hold(A) :- prob(    hold(A)).
0.5 :: not_hold(A) :- prob(not_hold(A)).

E/(E+1)  :: hold(A) :- prob(hold(A),W), E=2.71828182**(W/100000).

E/(E+1) :: whold(A) :- prob(whold(A),W), E=2.71828182**(W/100000).
bot :- prob(whold(A),W),     whold(A), not hold(A).
bot :- prob(whold(A),W), not whold(A),     hold(A).
