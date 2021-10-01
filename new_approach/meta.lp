%
% Meta-encoding
%

{ _h((P,X,V)) : _random(_, (P,X,V))} = 1 :- _random(_, (P,X, _)).

% { _h(A) : _random(E, A)} = 1 :- _random(E, _).

:- not _h(A), _obs(A).
:- not _h(A), _obs(A, true).
:- _h(A), _obs(A, false).

_h(A) :- _do(A).

_int((P,X)) :- _do((P,X,V)).
% _int((P,X)) :- _do(-(P,X,V)).

:- _h((P,X,_)), 2 { _h(P,X,V) }.
% -_h((P, X, V1)) :- _h((P,X,V2)), V1 != V2, _random(_, (P,X,V1)).


%
% Probabilities: TO MAXIMIZE
%
#const factor=5.
#const option=1.
% #const option=2.

%
% option = 1
%

% assigned probability
:~ _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)),     _pr(E,(P,X,V),Pr), option = 1. [-@log(Pr, factor),E,P,X]

:- _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)),     _pr(E,(P,X,V),Pr), option = 1, Pr=0.

% default numerator
:~ _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)), not _pr(E,(P,X,V),_), option = 1,
    Y = #sum { @intpr(Pr),V1 : _random(E,(_, X, V1)), _pr(E,(_,X,V1),Pr) }, Y>0.        [-@log(@frac(@intpr(1)-Y, @intpr(1)), factor),num,E,P,X]

:- _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)), not _pr(E,(P,X,V),_), option = 1,
    Y = #sum { @intpr(Pr),V1 : _random(E,(_, X, V1)), _pr(E,(_,X,V1),Pr) },             @intpr(1)-Y<=0.

% default denominator
:~ _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)), not _pr(E,(P,X,V),_), option = 1,
   M = #count { V1 : _random(E,(P,X,V1)), not _pr(E,(P,X,V1),_) }, M>1.                 [-@log(@frac(1,M), factor),den,E,P,X]

:- _random(E,(P,X,V)), _h((P,X,V)), not _int((P,X)), not _pr(E,(P,X,V),_), option = 1,
   M = #count { V1 : _random(E,(P,X,V1)), not _pr(E,(P,X,V1),_) },                      M=0.
% %
% % option = 2
% %
% #show _card/2.
% _no_int(E,(P,X))  :- _random(E,(P,X,_)), not _int((P,X)),                option = 2.
% _pr(E,(P,X),Pr)   :- _random(E,(P,X,V)), _h((P,X,V)), _pr(E,(P,X,V),Pr), option = 2.
% _default(E,(P,X)) :- _no_int(E,(P,X)), not _pr(E,(P,X)_),                option = 2.

% % assigned probability
% :~ _pr(E,(P,X),Pr), _no_int(E,(P,X)),                                    option = 2. -[@log(Pr),E,P,X]

% % default numerator
% :~ default(E,(P,X)), Y = #sum { Pr,A : _random(E,A), _pr(E,A,Pr) },      option = 2. -[@log(1-Y),E,P,X]

% % default denominator
% :~ default(E,(P,X)), M = #count{ A : _random(E,A), not _pr(E,A,_) },     option = 2.  [@log(M),E,P,X]

#script (python)
from clingo import Number, String
from math import log as mathlog

def log(a, factor):
    factor = factor.number
    ln = mathlog(float(eval(a.string)))
    weight = Number(int(ln * (10**factor)))
    return weight

def frac(n,d):
    return String(f'{n.number}/{d.number}')

def intpr(a):
    factor = 10**6
    if str(a.type) == 'SymbolType.String':
        return Number(int(float(eval(a.string))*factor))
    elif str(a.type) == 'SymbolType.Number':
        return Number(a.number*factor)
#end.