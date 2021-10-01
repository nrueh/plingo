% Sort declarations
boolean(t;f).

% Regular part

% Random selection rules
&random{ r1; male(B) : boolean(B) }.
&random{ r2; recover(B) : boolean(B) }.
&random{ r3; drug(B) : boolean(B) }.

% Probability atoms
&pr{ r1; male(t) } = "1/2".
&pr{ r2; recover(t) } = "0.6" :- male(t), drug(t).
&pr{ r2; recover(t) } = "0.7" :- male(t), drug(f).
&pr{ r2; recover(t) } = "0.2" :- male(f), drug(t).
&pr{ r2; recover(t) } = "0.3" :- male(f), drug(f).
&pr{ r3; drug(t) } = "0.75" :- male(t).
&pr{ r3; drug(t) } = "0.25" :- male(f).



% Observations and actions
&do{ drug(f) }.
