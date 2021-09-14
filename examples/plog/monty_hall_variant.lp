%%% P-Log program %%%
% Sort declarations
door(1..4).)

% Attributes
&attribute(open, (), door).
&attribute(selected, (), door).
&attribute(prize, (), door).

% Regular part
-canopen(D) :- selected(D).
-canopen(D) :- prize(D).
canopen(D) :- not -canopen(D), door(D).

% Random selection rules
&random(r1, prize, ()).
&random(r2, selected,()).
&random(r3, open, (canopen,)).

% Probability atoms
&pratom(prize(1), "0.3").
&pratom(prize(3), "0.2").

% Observations and actions
obs(selected(1)).
obs(open(2)).
obs(-prize(2)).