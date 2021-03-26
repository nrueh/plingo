% Rule conversions printed
unsat(0,"alpha",X) :- not bird(X); residentBird(X).
bird(X) :- not unsat(0,"alpha",X); residentBird(X).
:~ unsat(0,"alpha",X). [1@1]

unsat(1,"alpha",X) :- not bird(X); migratoryBird(X).
bird(X) :- not unsat(1,"alpha",X); migratoryBird(X).
:~ unsat(1,"alpha",X). [1@1]

unsat(2,"alpha",X) :- #true; residentBird(X); migratoryBird(X).
#false :- not unsat(2,"alpha",X); residentBird(X); migratoryBird(X).
:~ unsat(2,"alpha",X). [1@1]

unsat(3,2) :- not residentBird(jo); #true.
residentBird(jo) :- not unsat(3,2); #true.
:~ unsat(3,2). [2@0]

unsat(4,1) :- not migratoryBird(jo); #true.
migratoryBird(jo) :- not unsat(4,1); #true.
:~ unsat(4,1). [1@0]