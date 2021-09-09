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
&pratom(prize = 1) = 0.3.
&pratom(prize = 3) = 0.2.