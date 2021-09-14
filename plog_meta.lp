% Create attribute atoms without range
attribute(Name, Domain) :- attribute(Name, Domain, Range).
% attribute(Name) :- attribute(Name, Domain, Range).

% Unique value for each attribute
-hold(attribute(Name, Domain, sort(R, Y1))) :- hold(attribute(Name, Domain, sort(R, Y2))), Y1 != Y2, sort(R, Y1).

% fixed attributes will not be considered random
intervene(attribute(Name, Domain)) :- do(hold(attribute(Name, Domain, Range))).
intervene(attribute(Name, Domain)) :- do(-hold(attribute(Name, Domain, Range))).

% Generation rule for random rules without set term
1 {hold(attribute(Name, Domain, sort(Sort,Y))) : sort(Sort,Y)}1 :- random(_, Name), 
                                                                attribute(Name, Domain, sort(Sort,_)), 
                                                                not intervene(attribute(Name, Domain)).

% Generation rule for random rules with set term
1 {hold(attribute(Name, Domain, sort(Sort,Y))) : sort(Sort,Y), hold(SortTerm, sort(Sort, Y))}1 :- random(_, Name, SortTerm), 
                                                                attribute(Name, Domain, sort(Sort,_)), 
                                                                not intervene(attribute(Name, Domain)).

% Observations have to be true in the answer set
:- obs(hold(attribute(Name, Domain, Range))), not hold(attribute(Name,Domain,Range)).
:- obs(-hold(attribute(Name, Domain, Range))), not -hold(attribute(Name,Domain,Range)).

% Actions make literals true
hold(attribute(Name, Domain, Range)):- do(hold(attribute(Name, Domain, Range))).
-hold(attribute(Name, Domain, Range)):- do(-hold(attribute(Name, Domain, Range))).

% Possible atoms without set term
poss(RandomIdentifier, attribute(AttrName, Domain, Range)) :- attribute(AttrName, Domain, Range), 
                                                random(RandomIdentifier, AttrName),
                                                not intervene(attribute(AttrName, Domain)).

% Possible atoms with set term
poss(RandomIdentifier, attribute(AttrName, Domain, Range)) :- attribute(AttrName, Domain, Range), 
                                                random(RandomIdentifier, AttrName, SetTerm), hold(SetTerm, Range),
                                                not intervene(attribute(AttrName, Domain)).


% % TODO: Implement dynamic range
% % Assigned Probability
% posswithassprob(RandomIdentifier, Attr) :- pratom(RandomIdentifier, Attr, Prob), poss(RandomIdentifier, Attr).
% assprob(RandomIdentifier, Attr) :- hold(Attr), posswithassprob(RandomIdentifier, Attr).
% :~ not assprob(RandomIdentifier, Attr), pratom(RandomIdentifier, Attr, Prob). [@log(Prob)@0]
% posswithassprob(Attr) :- posswithassprob(RandomIdentifier, Attr).

% % Default probability
% posswithdefprob(Attr) :- poss(RandomIdentifier, Attr), not posswithassprob(RandomIdentifier, Attr).
% numdefprob(attribute(Name, Domain), X) :- hold(attribute(Name, Domain, sort(R, Y1))), 
%                                         posswithdefprob(attribute(Name, Domain, sort(R, Y1))),
%                                         X = #count{Y2 : posswithdefprob(attribute(Name, Domain, sort(R,Y2)))}.
% cardinality_numdefprob(M) :- numdefprob(_, M).

% :~ not numdefprob(attribute(Name, Domain), M), cardinality_numdefprob(M), attribute(Name, Domain), M>1. [@log(@frac(1,M))@0]

% % Numerator for default probability
% remprob(attribute(AttrName, Domain), 100-S) :- 
%                         Attr = attribute(AttrName, Domain, _),
%                         hold(Attr), 
%                         posswithdefprob(Attr), 
%                         S = #sum{@intprob(Prob) : posswithassprob(RandomIdentifier, attribute(Name, Domain, sort(R, Y))), pratom(RandomIdentifier, attribute(Name, Domain, sort(R, Y)), Prob)}.

% % remprob(attribute(AttrName, Domain), 100-S) :- random(RandomIdentifier, AttrName, SetTerm), 
% %                         Attr = attribute(AttrName, Domain, _),
% %                         hold(Attr), 
% %                         posswithdefprob(Attr), 
% %                         S = #sum{@intprob(Prob) : posswithassprob(RandomIdentifier, attribute(Name, Domain, sort(R, Y))), pratom(RandomIdentifier, attribute(Name, Domain, sort(R, Y)), Prob)}.

% totaldefprob(Attr2, X) :- remprob(Attr2, X), X > 0.
% :~ not totaldefprob(Attr2, X), remprob(Attr2, X). [@log(@frac(X,100))@0]
% :- remprob(Attr2, X), X <= 0.