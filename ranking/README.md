## Compute Ranking

This script compute the **ranking per student** using three specific information which are:

- Position of the last CUSCONTEST
- Codeforces rating
- Number of problems solved in codeforces

Additional for each information is considered a **weight** that can be edited in the script

#### Cuscontest Position Points

For each student `s`, these points consider position in the last **CUSCOTEST** by category i.e Beginner and Intermediate:

```math
PositionPoints_s = \left( { CuscotestTotalTeamsByCategory_s - Position_s + 1 \over CuscotestTotalTeamsByCategory_s }  \right) \left( PositionWeight \right)
```

#### Codeforces Ratng Points

```math
MaximumRating = \max_{1 \leq s \leq n} \left( Rating_s \right)
```

```math
RatingPoints_s = \left( {Rating_s \over MaximumRating }  \right) \left( RatingWeight \right)
```

#### Codeforces Solved Problems Points

Points for problems solved in codeforces will be calculated as follows:


```math
TotalSolvedProblems_s = \sum_{k=1}^p ProblemSolvedRating_k 
```

```math
MaximumProblemSolved = \max_{1 \leq s \leq n} \left( TotalSolvedProblems_s \right)
```

```math
ProblemsPoints_s = \left( {TotalSolvedProblems_s \over MaximumProblemSolved }  \right) \left( ProblemSolvedWeight \right)
```

#### Total Points

The total amount of points is simply the sum of the points mentioned above:

```math
TotalPoints_s = PositionPoints_s + RatingPoints_s + ProblemsPoints_s
```

## Document format

The excel document with the data for compute the ranking must have the following format:

| Code | Name | CuscontestPosition | CodeforcesHandle | Team | Category |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 204321 | Yishar Piero Nieto Barrientos | 1 | theFixer | Pancito | Intermediate |
| 231442 | Yamir Wagner Florez Vega | 1 | WagnerYFV | Net team  | Beginner |

## Install dependencies

Dependencies that must be installed before running the script are the following:

```bash
pip3 install openpyxl
pip3 install requests
pip3 install json
pip3 install tabulate
```

## Command to run

To run the script, it is necessary the path to the excel document that is sent through the `filepah` parameter. 

In this sense, the command to execute the script is the following:

``` bash
 python3 ranking.py [filepath]
```
