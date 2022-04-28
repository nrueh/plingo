bird(X) :- residentBird(X).
bird(X) :- migratoryBird(X).
:- residentBird(X), migratoryBird(X).
0.67::residentBird(jo).
0.33::migratoryBird(jo).
query(query).
query:-residentBird(jo).
