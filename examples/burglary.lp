burglary :- &log("0.1").
:- burglary,  &log("0.9").

earthquake :- &log("0.2").
:- earthquake, &log("0.8").

hears_alarm(X) :- person(X), &log("0.7").
:- hears_alarm(X), person(X), &log("0.3").

alarm :- burglary. 
alarm :- earthquake.
calls(X) :- alarm, hears_alarm(X).

person(mary).
person(john).

#show burglary/0.
#show earthquake/0.
#show hears_alarm/1.