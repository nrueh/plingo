#const days = 1.
% sorts
boolean(true;false).
patch(p1;p2).
day(1..days). 

% attributes

% hidden_in:#patch.
% found:#day->#boolean.
% look: #day->#patch.

%statements

&random { hidden_in(P) : patch(P) }.
&random { found(D,B) : boolean(B) } :- hidden_in(P), look(D,P).

found(D,false) :- hidden_in(P1), look(D,P2), P1!=P2.

&pr { hidden_in(p1) } = "0.8".
&pr { found(D,true) } = "0.2" :- day(D).

look(D,p1) :- day(D).

&obs { found(1,false) }.
% &obs { found(5,false) }.

#show hidden_in/1.
#show found/2.

&query(found(days,true)).
