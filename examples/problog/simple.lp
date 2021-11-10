p :- &log("0.6/0.4").
q :- &log("0.3/0.7").
% p :- &problog("0.6").
% q :- &problog("0.3").
r :- p.
r :- q.

&query(r).
