location(1..5).
#const query_to = 5.
#const blocks = 3.

%The grid is desribed by the relation leftof(location, location) and belowof(location, cation)

% 1 -- 2 -- 3

%      |    |

%      4 -- 5

leftof(1,2). leftof(2,3).
belowof(2,4). belowof(3,5).
leftof(4,5).
