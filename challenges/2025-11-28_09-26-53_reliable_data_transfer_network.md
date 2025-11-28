# Reliable Data Transfer Network

## Difficulty
Hard

## Description
A large company operates a network of `N` servers interconnected by `M` bidirectional fiber optic cables. Each cable connects two servers and has an associated installation `cost`. One of these servers is designated as the `Main Server` (server 0). Additionally, there are `K` `Backup Servers` that are critical for data redundancy.

Your task is to select a subset of these fiber optic cables such that two conditions are met, while minimizing the total installation cost of the selected cables:
1.  All `Backup Servers` must be connected to the `Main Server`.
2.  For every individual `Backup Server`, there must exist at least two *edge-disjoint* paths from the `Main Server` to that `Backup Server` using only the selected cables. This means if any single selected cable fails, each `Backup Server` will still have at least one path to the `Main Server`.

The problem asks for the minimum total `cost` of cables to install to satisfy these conditions. It is guaranteed that a solution always exists for the provided test cases.

## Constraints
*   `2 <= N <= 1000` (Number of servers)
*   `1 <= M <= 5000` (Number of potential cables)
*   `1 <= K < N` (Number of Backup Servers)
*   `0 <= server_id < N`
*   `server_0` is the `Main Server`.
*   `0 <= cost <= 10^9` for each cable.
*   All `Backup Servers` are distinct and not the `Main Server`.

## Test Cases

### Test Case 1
#### Input
```
4 4 2
0 1 10
0 2 10
1 3 5
2 3 5
Backup Servers: 1 2
```
#### Output
```
30
```

### Test Case 2
#### Input
```
3 3 1
0 1 100
1 2 10
0 2 20
Backup Servers: 2
```
#### Output
```
130
```

### Test Case 3
#### Input
```
5 5 1
0 1 10
1 2 10
2 3 10
3 4 10
0 4 50
Backup Servers: 4
```
#### Output
```
90
```

### Test Case 4
#### Input
```
5 8 2
0 1 10
0 2 10
0 3 10
1 4 5
2 4 5
3 4 5
1 2 50
0 4 100
Backup Servers: 2 4
```
#### Output
```
145
```

### Test Case 5
#### Input
```
6 9 2
0 1 10
0 2 10
0 3 10
0 4 10
1 5 1
2 5 1
3 5 1
4 5 1
Backup Servers: 1 2
```
#### Output
```
44
```