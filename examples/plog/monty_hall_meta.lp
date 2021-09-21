#include "../../plog_meta.lp".

% Sort declarations
sort(door, (1;2;3)).

% Attributes
attribute(open, domain(), sort(door, D)) :- sort(door, D).
attribute(selected, domain(), sort(door, D)) :- sort(door, D).
attribute(prize, domain(), sort(door, D)) :- sort(door, D).

% Regular part
-hold(canopen, sort(door, D)) :- hold(attribute(selected, domain(), sort(door, D))).
-hold(canopen, sort(door, D)) :- hold(attribute(prize, domain(), sort(door, D))).
hold(canopen, sort(door, D)) :- not -hold(canopen, sort(door, D)), sort(door,D).

% Random selection rules
random(r1, prize).
random(r2, selected).
random(r3, open, canopen).

% No probability atoms

% Observations and actions
obs(hold(attribute(selected, domain(), sort(door,1)))).
obs(hold(attribute(open, domain(), sort(door,2)))).
obs(-hold(attribute(prize, domain(), sort(door,2)))).

% Convert meta attributes back to readable output
open(D) :- hold(attribute(open, domain(), sort(_, D))).
selected(D) :- hold(attribute(selected, domain(), sort(_, D))).
prize(D) :- hold(attribute(prize, domain(), sort(_, D))).

#show open/1.
#show selected/1.
#show prize/1.