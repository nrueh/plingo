% Sort declarations
&sort(dice, (d1;d2)).
&sort(score, (1;2;3;4;5;6)).
&sort(person, (mike;john)).

% Attributes
&attribute(roll, (dice), score).
&attribute(owner, (dice,), person).
&attribute(even, (dice), boolean).

% Regular part
owner(d1, mike).
owner(d2, john).
even(D) :- roll(D,Y), Y \ 2 = 0.
-even(D) :- not even(D), dice(D).

% Random selection rules
random(r1, roll).
#show hold/1.

% % Probability atoms
% &pratom(roll(D, Y), "1/6") :- owner(D,john), score(Y).
% &pratom(roll(D, 6), "1/4") :- owner(D, mike).
% &pratom(roll(D, Y), "3/20") :- Y != 6, owner(D, mike).

% #show roll/2.
