% Model for a triplex steer-by-wire control system.

% Sorts
battery(batteryA; batteryB).
processor(processor1; processor2; processor3).
steering_sensor(steering_sensor1; steering_sensor2; steering_sensor3).
wheel_sensor(wheel_sensor1; wheel_sensor2; wheel_sensor3).
motor_controller(motor_controller1; motor_controller2).
two_of_three_voter(two_of_three_voter1; two_of_three_voter2).

% device = processor + motor + sensor.
device(D) :- processor(D).
device(D) :- motor_controller(D).
device(D) :- steering_sensor(D).
device(D) :- wheel_sensor(D).

% component = battery + processor + steering_sensor + wheel_sensor +
%                     + motor_controller + two_of_three_voter.

component(C) :- battery(C).
component(C) :- processor(C).
component(C) :- steering_sensor(C).
component(C) :- wheel_sensor(C).
component(C) :- motor_controller(C).
component(C) :- two_of_three_voter(C).

% component_status(intact; detected_broken; silent_broken).
broken_state(detected_broken; silent_broken).
boolean(true;false).

% Attributes
% connected: #component, #component -> #boolean.
% powered:   #device -> #boolean.
% status: #component -> #broken_state.
% operational: #component -> #boolean.
% system_failure: #boolean.

% **Introduced for modeling purposes**

% broken : #component -> #boolean.
% valid_world: #boolean.


% Statements

% **Connections**
connected(batteryA, processor1).
connected(batteryA, processor2).
connected(batteryA, steering_sensor1).
connected(batteryA, steering_sensor2).
connected(batteryA, wheel_sensor1).
connected(batteryA, wheel_sensor2).
connected(batteryA, motor_controller1).

connected(batteryB, processor2).
connected(batteryB, processor3).
connected(batteryB, streering_sensor2).
connected(batteryB, streering_sensor3).
connected(batteryB, wheel_sensor2).
connected(batteryB, wheel_sensor3).
connected(batteryB, motor_controller2).

% Processors 1, 2, and 3 are each connected to each two-of-three-voter. 
connected(P,V) :- processor(P), two_of_three_voter(V).

% Voter n is connected to motor-controler n for n in {1,2}.
connected(V, MC) :- two_of_three_voter(V), motor_controller(MC).

% Each sensor is connected to each processor.
connected(S, P):- processor(P), steering_sensor(S).
connected(W, P):- wheel_sensor(W), processor(P) .

% commutativity.
% connected(Component1, Component2) :- connected(Component2, Component1).

% *Power*

% A component is powered if and only if
% it is connected to an operational battery.
powered(C,true) :- connected(B,C), operational(B,true), battery(B).
powered(C,false) :- not powered(C,true), component(C).

% *Component status*
% Components may be broken, with the following probabilities: 
% i. battery:  1E-6
% ii. processor:  5E-7
% iii. motor controler : 1E-7
% iv. voter: 1E-7
% v. wheel sensor:   1E-7
% vi. steering sensor:  2E-6

&random(C) { broken(C,B) : boolean(B) } :- component(C).

&pr { broken(C,true) } = "1/1000000" :- battery(C).
&pr { broken(C,true) } = "5/10000000" :- processor(C). 
&pr { broken(C,true) } = "1/10000000" :- motor_controller(C). 
&pr { broken(C,true) } = "1/10000000" :- two_of_three_voter(C). 
&pr { broken(C,true) } = "1/10000000" :- wheel_sensor(C). 
&pr { broken(C,true) } = "2/1000000" :- steering_sensor(C). 

% *Component Operation*

% All components are normally operational
operational(C,true) :- not operational(C,false), component(C).

% Any processor, battery, motor controler, or sensor which is not powered
% is not operational.
operational(P,false) :- powered(P,false), processor(P).
operational(MC,false) :- powered(MC,false), motor_controller(MC).
operational(S,false) :- powered(S,false), steering_sensor(S).
operational(W,false) :- powered(W,false), wheel_sensor(W).

% Any component that is broken, either silently or detectably, is not operational.
&random { status(C,BS) : broken_state(BS) } :- broken(C,true), valid_world.
% 90% of breakages are detectable.
&pr { status(C,detected_broken) } = "9/10" :-  broken(C,true).

operational(C,false) :- broken(C,true).


% If two of the three processors connected to a two-of-three voter
% is non-operational, the voter is non-operational
operational(V,false) :- #count { 1,P : processor(P), connected(P,V), operational(P,false) } > 1, two_of_three_voter(V).

% *System failure*
% System failure occurs if one of the motor controlers is not operational,
system_failure :- operational(MC,false), motor_controller(MC).

% System failure occurs if two or more wheel sensors are non-operational
system_failure :- #count { 1,W: wheel_sensor(W), operational(W,false) } > 1.

% System failure occure if two or more steering sensors are non-operational. 
system_failure :- #count { 1,S: steering_sensor(S), operational(S,false) } > 1.

% we only consider possible worlds no more than four components fail 
valid_world :- #count { 1,C : broken(C,true) } < 5.
:- not valid_world.

% *Queries*
% Probability of failure
&query(system_failure).

