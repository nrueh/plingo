location(1..15).
#const query_to = 15.
#const blocks = 3.

%The grid is desribed by the relation leftof(location, location) and belowof(location, cation)

% 1 -- 2 -- 3 -- 4 -- 5

%      |    |    |	

% 6--  7 -- 8 -- 9 -- 10

%      |    |	 | 

% 11--12 --13 --14 -- 15


leftof(1,2). leftof(2,3). leftof(3,4). leftof(4,5).
belowof(2,7). belowof(3,8). belowof(4,9).
leftof(6,7). leftof(7,8). leftof(8,9). leftof(9,10).
belowof(7,12). belowof(8,13). belowof(9,14).
leftof(11,12). leftof(12,13). leftof(13,14). leftof(14,15).

