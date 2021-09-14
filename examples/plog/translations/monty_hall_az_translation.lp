% montyhall.lp
% Monty Hall Example to compute PLOG in lpmln2asp
% command line: lpmln2asp -i montyhall.lp -q prize
% Last modified: 06/23/2017
% Section 4.2

door(d1;d2;d3).
constant(prize;selected;open).
number(2;3).
boolean(t;f).

canopen(D,f) :- selected(D),door(D).
canopen(D,f) :- prize(D),door(D).
canopen(D,t) :- not canopen(D,f),door(D),door(D).

:- canopen(D,t) , canopen(D,f).
:- prize(D1) , prize(D2) , D1!=D2.
:- selected(D1) , selected(D2) , D1!=D2.
:- open(D1) , open(D2) , D1!=D2.

prize(d1) :- not intervene(prize) , not prize(d2) , not prize(d3).
prize(d2) :- not intervene(prize) , not prize(d1) , not prize(d3).
prize(d3) :- not intervene(prize) , not prize(d2) , not prize(d1).

selected(d1) :- not selected(d2) , not selected(d3) , not intervene(selected).
selected(d2) :- not selected(d3) , not selected(d1) , not intervene(selected).
selected(d3) :- not selected(d2) , not selected(d1) , not intervene(selected).

open(d3) :- not open(d1) , not open(d2) , not intervene(open).
open(d2) :- not open(d1) , not open(d3) , not intervene(open).
open(d1) :- not open(d3) , not open(d2) , not intervene(open).

:- open(D) , not canopen(D,t) , not intervene(open).

posswithdefprob(selected,D) :- not posswithassprob(selected,D) , not intervene(selected),door(D),door(D).
posswithdefprob(prize,D) :- not posswithassprob(prize,D) , not intervene(prize),door(D),door(D).
posswithdefprob(open,D) :- not posswithassprob(open,D) , canopen(D,t) , not intervene(open),door(D) , door(D),door(D).

numdefprob(prize,X) :- X= #count{D:posswithdefprob(prize,D)} , prize(Y) , posswithdefprob(prize,Y).%,number(X).
numdefprob(selected,X) :- X= #count{D:posswithdefprob(selected,D)} , selected(Y) , posswithdefprob(selected,Y). %,number(X).
numdefprob(open,X) :- X= #count{D:posswithdefprob(open,D)} , open(Y) , posswithdefprob(open,Y).%,number(X).

do(selected,d1).
selected(d1) :- do(selected,d1).
intervene(selected) :- do(selected,d1).

obs(open,d2).
:- obs(open,d2) , not open(d2).

:- not numdefprob(C,2),constant(C), &weight("-0.6931").
:- not numdefprob(C,3),constant(C), &weight("-0.4054").

&query(prize(D)) :- prize(D).