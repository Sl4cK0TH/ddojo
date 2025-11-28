# Quantum Grid Navigation
## Difficulty
Hard
## Description
You are tasked with programming an advanced quantum robot to navigate an `M`x`N` grid. The robot starts at `(start_r, start_c)` with an initial energy `E` and must reach `(end_r, end_c)`.

Each cell `(r, c)` in the grid has an associated energy cost `C[r][c]` to *enter* it. A positive `C[r][c]` means energy is consumed, while a negative `C[r][c]` means energy is gained (e.g., from a passive energy field). Some cells are obstacles, represented by a very large positive cost (e.g., `2000000000`), which means they cannot be entered.

Additionally, some cells are "recharge stations" `S[r][c]`. If `S[r][c]` is `1`, the cell is a recharge station; otherwise, it's `0`. Upon entering a recharge station, the robot gains an *additional* fixed amount of energy `R`. However, there's a critical constraint: recharge stations can be used at most `K` times *in total* throughout the entire path (not per station, but cumulatively across all visited recharge stations). Once a recharge station is used on a path, it contributes to the `K` limit for that path.

The robot can only move to adjacent cells (up, down, left, right). Its energy level must *never drop below zero* after entering any cell and processing all energy changes (cost `C[r][c]` and potential `R` from `S[r][c]`).

Your goal is to find the *minimum initial energy `E`* the robot needs to successfully reach `(end_r, end_c)`. If it's impossible to reach the destination under these constraints, return `-1`.

## Grading Criteria
- **Correctness (60 points):** Awarded for passing the 5 visible test cases (12 points each).
- **Code Quality (20 points):** Awarded by an AI review for clean, non-hardcoded code.
- **Efficiency (20 points):** Awarded by an AI review for using an optimal algorithm (judged by Big O complexity).

## Constraints
*   `1 <= M, N <= 50`
*   `0 <= K <= 10`
*   `0 <= R <= 1000`
*   `-1000 <= C[r][c] <= 1000` for regular cells. Obstacles are marked with `C[r][c] = 2000000000`.
*   `S[r][c]` is `0` or `1`.
*   `0 <= start_r, end_r < M`
*   `0 <= start_c, end_c < N`
*   ` (start_r, start_c) ` and ` (end_r, end_c) ` are distinct and not obstacles.
*   The robot begins at ` (start_r, start_c) ` with `E` initial energy *before* moving to any other cell. The cost of ` (start_r, start_c) ` itself is not incurred initially.

## Test Cases
### Test Case 1
#### Input
```
3 3 0 100
1 1 1
1 1 1
1 1 1
0 0 0
0 0 0
0 0 0
0 0 2 2
```
#### Output
```
4
```
*Explanation: No recharges available (K=0). The shortest path from (0,0) to (2,2) involves 4 moves, each costing 1 energy. The maximum energy deficit occurs after the 4th move, requiring an initial energy of 4.*

### Test Case 2
#### Input
```
3 3 1 10
1 1000 1
1 100 1
1 1000 1
0 0 0
0 1 0
0 0 0
0 0 2 2
```
#### Output
```
93
```
*Explanation: The direct path through (0,1) or (2,1) has high costs (1000). The path through (1,1) (cost 100, recharge +10) becomes more viable. Path: (0,0)->(1,0)->(1,1 [recharge])->(2,1)->(2,2). The maximum energy deficit occurs when entering (1,1), which costs 100 but gains 10, a net cost of 90. When coming from (1,0) (net -1 energy), an additional 90 net cost makes the balance -91. This means 91 initial energy is needed to stay non-negative. This is the bottleneck for this path, and the overall minimum is 93 after covering costs of subsequent cells.*

### Test Case 3
#### Input
```
4 4 1 5
1 1 1 1
1 2000000000 1 1
1 1 1 1
1 1 1 1
0 0 0 0
0 0 1 0
0 0 0 0
0 0 0 0
0 0 3 3
```
#### Output
```
2
```
*Explanation: There's an obstacle at (1,1). The path (0,0)->(0,1)->(0,2)->(1,2 [recharge])->(2,2)->(3,2)->(3,3) uses one recharge.
The costs are 1, 1, (1-5=-4), 1, 1, 1.
The balance becomes: 0 -> -1 -> -2 -> -2 - (-4) = 2 -> 1 -> 0 -> -1.
The maximum initial energy needed is 2 (to cover the initial -2 balance before the recharge, and then -1 after the last cell).*

### Test Case 4
#### Input
```
3 3 1 10
1 2000000000 1
2000000000 2000000000 2000000000
1 2000000000 1
0 0 0
0 0 0
0 0 0
0 0 2 2
```
#### Output
```
-1
```
*Explanation: The grid structure makes it impossible to move from (0,0) to (2,2) due to surrounding obstacles.*

### Test Case 5
#### Input
```
4 4 2 20
1 -5 1 1
-5 100 1 1
1 1 -5 1
1 1 1 -5
0 0 0 0
0 1 0 0
0 0 0 0
0 0 0 0
0 0 3 3
```
#### Output
```
0
```
*Explanation: The grid contains several cells with negative costs, meaning entering them grants energy. One optimal path (0,0)->(0,1)->(0,2)->(0,3)->(1,3)->(2,3)->(3,3)
Path costs: C(0,1)=-5, C(0,2)=1, C(0,3)=1, C(1,3)=1, C(2,3)=1, C(3,3)=-5.
Energy balance (starting with 0 initial):
0 (at 0,0)
-> 0 - (-5) = 5 (at 0,1)
-> 5 - 1 = 4 (at 0,2)
-> 4 - 1 = 3 (at 0,3)
-> 3 - 1 = 2 (at 1,3)
-> 2 - 1 = 1 (at 2,3)
-> 1 - (-5) = 6 (at 3,3)
The balance never drops below 0. Thus, 0 initial energy is sufficient.*