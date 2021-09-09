%%% P-Log program %%%
% % Sort declarations
% door = {1,2,3}.

% % Attributes
% open: door.
% selected: door.
% prize: door.

% % Regular part
% -canopen(D) :- selected(D).
% -canopen(D) :- prize(D).
% canopen(D) :- not -canopen(D).

%% Random selection rules
% random(roll(D)).

% % Random selection rules
% random(prize).
% random(selected).
% random(open : {X: canopen(X)}).

% Observations and actions
% obs(selected(1)).
% obs(open(2)).
% obs(-prize(2)).

%%% Translation to ASP %%%
% Sort declarations
door(1;2;3).
attr(open;selected;prize).

% Regular part
-canopen(D) :- selected(D).
-canopen(D) :- prize(D).
canopen(D) :- not -canopen(D), door(D).

% Unique value for each attribute
-open(D1) :- open(D2), D1 != D2, door(D1).
-selected(D1) :- selected(D2), D1 != D2, door(D1).
-prize(D1) :- prize(D2), D1 != D2, door(D1).

% Fixed attributes will not be considered random
intervene(open) :- do(open(D)).
intervene(selected) :- do(selected(D)).
intervene(prize) :- do(prize(D)).

% Random selection rules
1 {prize(D) : door(D)} 1 :- not intervene(prize).
1 {selected(D) : door(D) } 1 :- not intervene(selected).
1 {open(D) : door(D), canopen(D)} 1 :- not intervene(open).

% Observations and actions
obs(selected(1)).
obs(open(2)).
obs(-prize(2)).

% Observations have to be true in the answer set
:- obs(open(D)), not open(D).
:- obs(-open(D)), not -open(D).
:- obs(selected(D)), not selected(D).
:- obs(-selected(D)), not -selected(D).
:- obs(prize(D)), not prize(D).
:- obs(-prize(D)), not -prize(D).

% Actions make literals true
open(D) :- do(open(D)).
selected(D) :- do(selected(D)).
prize(D) :- do(prize(D)).

#show prize/1.
#show open/1.
#show selected/1.

%%% Translation to LPMLN %%%
% Possible Atoms
poss(r1, prize(D)) :- not intervene(prize), door(D).
poss(r2, selected(D)) :- not intervene(selected), door(D).
poss(r3, open(D)) :- canopen(D), not intervene(open), door(D).

% Denominator for Default Probability
posswithdefprob(prize(D)) :- poss(r1, prize(D)), not posswithassprob(prize(D)).
posswithdefprob(selected(D)) :- poss(r2, selected(D)), not posswithassprob(selected(D)).
posswithdefprob(open(D)) :- poss(r3, open(D)), not posswithassprob(open(D)).

numdefprob(prize, X) :- prize(D), posswithdefprob(prize(D)), X=#count{Y : posswithdefprob(prize(Y))}.
numdefprob(selected, X) :- selected(D), posswithdefprob(selected(D)), X=#count{Y : posswithdefprob(selected(Y))}.
numdefprob(open, X) :- open(D), posswithdefprob(open(D)), X=#count{Y : posswithdefprob(open(Y))}.

:- not numdefprob(C,2),attr(C), &log("1/2").
:- not numdefprob(C,3),attr(C), &log("1/3").