function pseudoRandomizedList =  pseudoRand(conditions, repetitions)
% pseudoRandomizedList =  pseudoRand(conditions, repetitions)
% 
% pseudoRand creates a vector of shuffled conditions repeated a set number
% of times. Within each repetition, all the conditions are presented
% exactly once.
% 
% Leonardo Lupori 2020
% 
% see also: randperm



% Initialize the randomized final list
pseudoRandomizedList = zeros(length(conditions),repetitions);

% Randomly permute the order of the conditions for every repetition
for i = 1:repetitions
    pseudoRandomizedList(:,i) = conditions(randperm(length(conditions)));
end

% Expand the list to a single dimension
pseudoRandomizedList = pseudoRandomizedList(:);