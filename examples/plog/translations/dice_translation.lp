%%%%%% P-Log program %%%%%%
%% Sort declarations 
% dice = {d1,d2}.
% score = {1,2,3,4,5,6}.
% person = {mike,john}.

%% Attributes
% roll: dice --> score.
% owner: dice --> person.
% even: dice --> boolean.

%% Regular part
% owner(d1) = mike.
% ownder(d2) = john.
% even(D) :-  roll(D) = Y, Y mod 2 = 0.
% -even(D) :- not even(D).

%% Random selection rules
% random(roll(D)).

%% Probability atoms
% pr(roll(D) = Y | owner(D) = john) = 1/6.
% pr(roll(D) = 6 | owner(D) = mike) = 1/4.
% pr(roll(D) = Y | Y != 6, owner(D) = mike) = 3/20.


%%%%%% Translation to ASP %%%%%%
% Sort declarations
dice(d1;d2).
score(1;2;3;4;5;6).
person(mike;john).
% boolean(t;f).

% Regular part
owner(d1,mike).
owner(d2,john).
even(D) :- roll(D,Y), Y \ 2 = 0.
-even(D) :- not even(D), dice(D).

% Unique value for each attribute
-roll(D,Y1) :- roll(D,Y2), Y1 != Y2, score(Y1).
-owner(D,P1) :- owner(D,P2), P1 != P2, person(P1).

% fixed attributes will not be considered random
intervene(roll(D)) :- do(roll(D,Y)).
intervene(owner(D)) :- do(owner(D,Y)).
intervene(even(D)) :- do(even(D,Y)).

% Random selection rule
1 {roll(D,Y) : score(Y)}1 :- not intervene(roll(D)), dice(D).

% Rule for dynamic range omitted since no dynamic range

% Observations and actions
obs(roll(d2,1)).

% Observations have to be true in the answer set
:- obs(roll(D,Y)), not roll(D,Y).
:- obs(-roll(D,Y)), not -roll(D,Y).
:- obs(owner(D,P)), not owner(D,P).
:- obs(-owner(D,P)), not -owner(D,P).
:- obs(even(D,B)), not even(D,B).
:- obs(-even(D,B)), not -even(D,B).

% Actions make literals true
roll(D,Y) :- do(roll(D,Y)).
owner(D,P) :- do(owner(D,P)).
even(D,B) :- do(even(D,B)).

%%%%%% Translation to LPMLN %%%%%%
% Possible atoms
poss(r1,roll(D, Y)) :- score(Y), not intervene(roll(D)), dice(D).

% Assigned probability
% posswithassprob(r1, owner(D,john), roll(D,Y)) :- poss(r1, roll(D,Y)), owner(D,john).
posswithassprob(r1, owner(D,mike), roll(D, 6)) :- poss(r1, roll(D, 6)), owner(D, mike).

asspr(r1, owner(D,john), roll(D,Y)) :- roll(D,Y), posswithassprob(r1,owner(D,john), roll(D,Y)).
asspr(r1, owner(D,mike), roll(D,Y)) :- roll(D,Y), posswithassprob(r1, owner(D,mike), roll(D,Y)).

:- not asspr(r1, owner(D,john), roll(D,Y)), dice(D), score(Y), &log("1/6").
:- not asspr(r1, owner(D,mike), roll(D,Y)), dice(D), score(Y), Y=6, &log("1/4").
:- not asspr(r1, owner(D,mike), roll(D,Y)), dice(D), score(Y), Y!=6, &log("3/20").

posswithassprob(Attr) :- posswithassprob(R,C,Attr).

% Default probability
posswithdefprob(roll(D, Y)) :- poss(r1, roll(D, Y)), not posswithassprob(r1, _, roll(D, Y)).
numdefprob(roll(D), X) :- roll(D, Y), posswithdefprob(roll(D, Y)), X = #count{Z : posswithdefprob(roll(D,Z))}.

:- not numdefprob(roll(D), 2), dice(D), &log("1/2").
:- not numdefprob(roll(D), 3), dice(D), &log("1/3").
:- not numdefprob(roll(D), 4), dice(D), &log("1/4").
:- not numdefprob(roll(D), 5), dice(D), &log("1/5").
:- not numdefprob(roll(D), 6), dice(D), &log("1/6").

% Numerator for default probability
remprob(roll(D), 100-Z) :- roll(D, Y), posswithdefprob(roll(D, Y)), Z = #sum{25 : posswithassprob(r1, owner(D, mike), roll(D, 6))}.
totaldefprob(roll(D), X) :- remprob(roll(D), X), X > 0. 
:- not totaldefprob(roll(d1), 75),  &log("0.75").
:- not totaldefprob(roll(d1), 100),  &log("1").
% &query(roll(D,Y)) :- roll(D,Y).
#show roll/2.