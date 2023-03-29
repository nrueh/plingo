location(1..10).
#const query_to = 10.
#const blocks = 1.

%The grid is desribed by the relation leftof(location, location) and belowof(location, cation)

% 1 -- 2 -- 3 -- 4 -- 5

%      |    |	 |	

% 6--  7 -- 8 -- 9 -- 10



leftof(1,2). leftof(2,3). leftof(3,4). leftof(4,5). 
belowof(2,7). belowof(3,8). belowof(4,9).
leftof(6,7). leftof(7,8). leftof(8,9). leftof(9,10).
