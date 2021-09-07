% Based on https://dtai.cs.kuleuven.be/problog/tutorial/various/01_montyhall.html

:- not {prize(1); prize(2); prize(3)} = 1.
:- prize(D), &problog("2/3").

% prize(1) :- &problog("1/3").
% prize(2) :- &problog("1/3").
% prize(3) :- &problog("1/3").

select_door(1).

{open_door(A) ; open_door(B)} = 1 :-
  A = 1..3,
  B = 1..3,
  A < B,
  not prize(A), not prize(B),
  not select_door(A), not select_door(B),
  &problog("1/2").

open_door(A) :-
  A = 1..3,
  B = 1..3,
  not prize(A), prize(B),
  not select_door(A), not select_door(B).

win_keep :-
  select_door(A),
  prize(A).

win_switch :-
  A = 1..3,
  not select_door(A),
  prize(A),
  not open_door(A).

&query(prize(P)) :- prize(P).
% &query(select_door(D)) :- select_door(D).
&query(win_keep).
&query(win_switch).