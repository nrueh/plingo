% Random block problem
% This a model for the random placement of blocks,
% which serve as obstacles, on the location of a map,
% and the resulting accessiblility relation among the locations.

% Sorts
% #const blocks = 1.

block(1..blocks).

% The domain contains only one random attributes
% which determines the location of the blocks

% Attributes

% place:#block -> #location.
% leftof: #location, #location -> #bool.
% belowof: #location, #location -> #bool.
% connected: #location, #location ->#bool.
% blocked: #location -> #bool.

% Statements

% Blocks are randomly placed
&random(B) { place(B,L) : location(L) } :- block(B).
#show place/2.

% Blocks are not distinguishable
:- place(B1,L1), place(B2,L2), B1<B2, L1<=L2.

% If some location has a block, it is blocked
blocked(L):- place(B,L).

% 'connected' is defined by the graph and if neither location has a block
connected(L1,L2) :- leftof(L1,L2), not blocked(L1), not blocked(L2).
connected(L1,L2) :- belowof(L1,L2), not blocked(L1), not blocked(L2).

% The relation connected is a symmetric and transitive relation
connected(L1,L2) :- connected(L2,L1), L1!=L2.
connected(L1,L3) :- connected(L1,L2), connected(L2,L3), L1!=L3.

