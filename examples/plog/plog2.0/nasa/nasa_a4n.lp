% Model for a triplex steer-by-wire control system.

% Sorts
battery(b1;b2).
processor(p1;p2;p3).
motor_controller(mc1;mc2).
steering_sensor(ss1; ss2; ss3).
wheel_sensor(ws1; ws2; ws3).
two_of_three_voter(v1; v2).

component(C) :- battery(C).
component(C) :- processor(C).
component(C) :- motor_controller(C).
component(C) :- steering_sensor(C).
component(C) :- wheel_sensor(C).
component(C) :- two_of_three_voter(C).

boolean(true;false).

% Attributes

% broken : #component -> #boolean.
% lessthan5broken :#boolean.

% Statements

% *Component status*
% Components may be broken, with the following probabilities: 
% i. battery:  1E-6
% ii. processor:  5E-7
% iii. motor controler : 1E-7
% iv. voter: 1E-7
% v. wheel sensor:   1E-7
% vi. steering sensor:  2E-6

&random { broken(C,B) : boolean(B) } :- component(C). 
#show broken/2.

&pr { broken(C,true) } = "1/1000000" :- battery(C).
&pr { broken(C,true) } = "5/10000000" :- processor(C). 
&pr { broken(C,true) } = "1/10000000" :- motor_controller(C). 
&pr { broken(C,true) } = "1/10000000" :- two_of_three_voter(C). 
&pr { broken(C,true) } = "1/10000000" :- wheel_sensor(C). 
&pr { broken(C,true) } = "2/1000000" :- steering_sensor(C). 



lessthan5broken :- #count { 1,C : broken(C,true) } < 5.
#show lessthan5broken/0.

&query(lessthan5broken).
