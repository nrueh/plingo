bird(X) :- residentBird(X).
bird(X) :- migratoryBird(X).
:- residentBird(X), migratoryBird(X). 

:~ residentBird(jo). [2@0]
:~ migratoryBird(jo). [5@0]