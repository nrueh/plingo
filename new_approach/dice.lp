%*
sorts

#dice={d1,d2}.
#score={1,2,3,4,5,6}.
#person={mike,john}.
*%
dice(d1;d2).
score(1..6).
person(mike,john).


%*
attributes

roll:#dice->#score.
owns:#dice,#person->#bool.
*%

% statements

owns(d1,mike).
owns(d2,john).

% random(roll(D, )).
%
%&random{ roll(D,X) : score(X) } :- dice(D).
%
_random(r1,(roll,D,X)) :- score(X), dice(D).

% probability information

% pr(roll(D)=6|owns(D,mike))=1/4.
% &pr{ roll(D,6) } = 1.4  :- owns(D,mike).
%
% Probability atoms
_pr(r1,(roll,D,X),"1/6") :- owns(D,john), score(X).
_pr(r1,(roll,D,6),"1/4") :- owns(D,mike).
_pr(r1,(roll,D,X),"3/20") :- X !=6, score(X), owns(D,mike).


% ? roll(d2)=6.

%
% Additional
%
_h((roll,D,S)) :- roll(D, S).
roll(D,S) :- _h((roll,D, S)).


% &obs { roll(d1,1) }.
_obs((roll,d2,1)).

% &do { roll(d1,1) }.
% _do((roll,d1,1)).

#show roll/2.

