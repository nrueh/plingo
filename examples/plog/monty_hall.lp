% Sort declarations
&sort(door, (1;2;3)).
&setterm(canopen, door).

% Attributes
&attribute(open, (), door).
&attribute(selected, (), door).
&attribute(prize, (), door).

% Regular part
-canopen(D) :- selected(D).
-canopen(D) :- prize(D).
canopen(D) :- not -canopen(D), door(D).

% Random selection rules
random(r1, prize).
random(r2, selected).
random(r3, open, (canopen)).

% No probability atoms

% Observations and actions
obs(selected(1)).
obs(open(2)).
obs(-prize(2)).

#show selected/1.
#show open/1.
#show prize/1.