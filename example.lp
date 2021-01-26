bird(X) :- residentBird(X).
bird(X) :- migratoryBird(X).
:- residentBird(X), migratoryBird(X). 

residentBird(jo).
migratoryBird(jo).

% &weight(2) { residentBird(jo) }.
% &weight(1) { migratoryBird(jo) }.