This is a solution to 8-puzzle problem using A_star algorithm
Start.txt contains the starting state
Goal.txt contains the final state
The algorithm first try to figure out wether it is solvable or not by counting number of inversions between start and goal state. If number of inversion is odd not solvable
If solvable then it solves using 1) Manhattan distance 2)Manhatten distance with added zero tile 3) Displacement tiles 4) Displacement tile heuristic  with added zero tiles
It returns the optimal path 
Optimal cost to reach from start to goal state( Parent to immediate child path cost uniform 1)
It also checks monotonic restriction is maintained or not
