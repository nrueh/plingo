#const cards = 4.

% Sorts
step(1..5).
kind(diamonds;clubs;hearts;spades).
% kind(1..4).

number(1..cards).
card((K,N)) :- kind(K), number(N).


% Card kind and number are encoded as single value
% card(X) :- X = (K-1) * cards + N, kind(K), number(N).
% #show card/1.

% Attributes
% draw: #step ->#card.

% Statements

&random(S) { draw(S,C) : card(C) } :- step(S).
#show draw/2.

% Cards cannot be drawn twice and order does not matter
:- draw(S1,C1), draw(S2,C2), S1 < S2, C1<=C2.

pair(S1,S2) :- draw(S1,(K1,N)), draw(S2,(K2,N)), S1<S2.
% :- #count { 1,S1,S2: pair(S1,S2) } != 1.

singlepair :- #count { 1,S1,S2: pair(S1,S2) } = 1.
% :- not singlepair.

&query(singlepair).

