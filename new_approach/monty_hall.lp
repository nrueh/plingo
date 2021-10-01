% Sort declarations
door(1..3).

% Regular part
-canopen(D) :- selected(D).
-canopen(D) :- prize(D).
canopen(D) :- not -canopen(D), door(D).

% Random selection rules
_random(r1, (prize,(),D)) :- door(D).
_random(r2, (selected,(),D)) :- door(D).
_random(r3, (open,(),D)) :- canopen(D).

% No probability atoms

% Observations and actions
_obs((selected,(),1)).
_obs((open,(),2)).
% &obs { prize(2), false }.
_obs((prize,(),2), false).

%
% Additional
%
_h((prize,(),D)) :- prize(D).
prize(D) :- _h((prize,(),D)).

_h((selected,(),D)) :- selected(D).
selected(D) :- _h((selected,(),D)).

_h((open,(),D)) :- open(D).
open(D) :- _h((open,(),D)).


#show selected/1.
#show open/1.
#show prize/1.