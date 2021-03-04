% Rule conversions printed
unsat(0,"alpha") :- residentBird(X); not bird(X).
bird(X) :- residentBird(X); not unsat(0,"alpha").
:~ unsat(0,"alpha"). [1@1]

unsat(1,"alpha") :- migratoryBird(X); not bird(X).
bird(X) :- migratoryBird(X); not unsat(1,"alpha").
:~ unsat(1,"alpha"). [1@1]

unsat(2,"alpha") :- residentBird(X); migratoryBird(X); not #false.
#false :- residentBird(X); migratoryBird(X); not unsat(2,"alpha").
:~ unsat(2,"alpha"). [1@1]

unsat(3,2) :- not residentBird(jo).
residentBird(jo) :- not unsat(3,2).
:~ unsat(3,2). [2@0]

unsat(4,5) :- not migratoryBird(jo).
migratoryBird(jo) :- not unsat(4,5).
:~ unsat(4,5). [5@0]


% Grounder output
% unsat(4,1):-not migratoryBird(jo).
% migratoryBird(jo):-not unsat(4,1).
% :~unsat(4,1).[1@0]

% unsat(3,2):-not residentBird(jo).
% residentBird(jo):-not unsat(3,2).
% :~unsat(3,2).[2@0]

% :-migratoryBird(jo),residentBird(jo).

% unsat(1,"alpha"):-migratoryBird(jo),not bird(jo).
% :~unsat(1,"alpha").[1@1]
% bird(jo):-not unsat(1,"alpha"),migratoryBird(jo).

% bird(jo):-not unsat(0,"alpha"),residentBird(jo).
% unsat(0,"alpha"):-residentBird(jo),not bird(jo).
% :~unsat(0,"alpha").[1@1]