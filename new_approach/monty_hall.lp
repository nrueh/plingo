% Sort declarations
door(1..3).

% Regular part
-canopen(D) :- selected(D).
-canopen(D) :- prize(D).
canopen(D) :- not -canopen(D), door(D).

% Random selection rules
&random{ r1; prize(D) : door(D) }.
&random{ r2; selected(D) : door(D) }.
&random{ r3; open(D) : canopen(D) }.

% No probability atoms

% Observations and actions
&obs{ selected(1) }.
&obs{ open(2) }.
&obs{ prize(2); false }.
