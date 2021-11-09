%
% Meta-encoding
%

{ _lpmln_h(A) : _lpmln_random(E,A)} = 1 :- _lpmln_random(E,_).

:- not _lpmln_h(A), _lpmln_obs(A,true).
:- _lpmln_h(A),     _lpmln_obs(A,false).

_lpmln_h(A) :- _lpmln_do(A).

_lpmln_int((P,X)) :- _lpmln_do((P,X,V)).


%
% Probabilities
%

_lpmln_no_int(E)  :- _lpmln_random(E,(P,X,_)), not _lpmln_int((P,X)).
_lpmln_pr(E,Pr)   :- _lpmln_random(E,A),_lpmln_h(A), _lpmln_pr(E,A,Pr).
_lpmln_default(E) :- _lpmln_no_int(E), not _lpmln_pr(E,_).

_lpmln_numsum(E,Y) :- _lpmln_default(E), Y = #sum { @intpr(Pr),A : _lpmln_random(E,A), _lpmln_pr(E,A,Pr) }.
_lpmln_densum(E,M) :- _lpmln_default(E), M = #count{ A : _lpmln_random(E,A), not _lpmln_pr(E,A,_) }.

% assigned probability
:~ _lpmln_pr(E,Pr), _lpmln_no_int(E).       [   -@log(Pr,_lpmln_factor),E]
:- _lpmln_pr(E,Pr), _lpmln_no_int(E),           Pr = 0.

% default numerator
:~ _lpmln_numsum(E,Y), @intpr(1)-Y > 0.   [-@log(@frac(@intpr(1)-Y,@intpr(1)),_lpmln_factor),num,E]
:- _lpmln_numsum(E,Y),                    @intpr(1) - Y <= 0.

% default denominator
:~ _lpmln_densum(E,M), M > 1.             [-@log(@frac(1,M),_lpmln_factor),den,E]
:- _lpmln_densum(E,M),                    M = 0.


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
