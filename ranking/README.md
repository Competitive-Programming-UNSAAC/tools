## Compute Ranking

This script compute the **ranking per student** using three specific information which are:

- Position of the **Selective Contest** (70 pts)
- Number of problems solved in codeforces (20 pts)
- Codeforces rating (10 pts)

Additional for each information is considered a **weight** that can be edited in the config file.

### Selective Contest Position Points

For each student `s`, these points consider position in the **Selective Contest**:

```math
PositionPoints_s = \left( { ContestTotalTeams_s - Position_s + 1 \over ContestTotalTeams_s }  \right) \left( PositionWeight \right)
```

### Codeforces Rating Points

If `n` students are participating in the selection. For each student `s`, these points will be the **Codeforces rating information obtained by the student in the different contests**.

The **minimum rating considered is 800**, that is, anyone who has **less than this rating bydefault will have 800**. 

```math
MaximumRating = \max_{1 \leq s \leq n} \left( Rating_s \right)
```

```math
RatingPoints_s = \left( { \max \left( 800, Rating_s \right)  \over MaximumRating }  \right) \left( RatingWeight \right)
```

### Codeforces Solved Problems Points

If `n` students are participating in the selection and a student solved `p` problems in Codeforces. For each student `s`, these points will be computed considering the number of problems solved and the rating of each problem i.e **hard problems give more points than easy problems**

Those **Gym problems that were solved during the training contest due to not having a rating will be considered the rating of 1000 points**.

```math
TotalSolvedProblems_s = \sum_{k=1}^p ProblemSolvedRating_k 
```

```math
MaximumProblemSolved = \max_{1 \leq s \leq n} \left( TotalSolvedProblems_s \right)
```

```math
ProblemsPoints_s = \left( {TotalSolvedProblems_s \over MaximumProblemSolved }  \right) \left( ProblemSolvedWeight \right)
```

### Total Points

For each student `s`, the total amount of points is simply the **sum of the points** mentioned above:

```math
TotalPoints_s = PositionPoints_s + RatingPoints_s + ProblemsPoints_s
```

## Selection Rules

For selection, students have to take into account the following `requirements`:

1. The student must **keep in mind that he or she will miss classes** in different courses during the event. Additionally, **upon returning the student must complete all pending assignments and exams** for the course.

2. Financial support will be requested from the university. However, not all event expenses will be covered, the student **must cover the expenses with their own money (transportation tickets, accommodation and food)**.

3. In the case of the student have financial support from the university. **Upon returning, the student must report to the university for the expenses incurred**.

Taking this into account, **8 slots will be available** and will be filled as follows:

- _Case #1_: **4 spots** will be filled with students who have **more than 110 accumulated credits** (from the 6th semester forward).

- _Case #2_: **3 spots** will be filled with students who have **less than or equal to 110 accumulated credits** (from the 1st semester to the 5th semester).

- _Case #3_: **1 spot** will be filled with a **woman student**.

For each of the `cases` mentioned above, the selection rule will be as follows:

1. The slots will be filled taking into account the ranking generated.
2. If a student does not meet the requirements, the slot will be assigned to the next one in the ranking.
3.  If there are no more students in the ranking for that case. The slot will be assigned for another case following the order _Case #1_, _Case #2_ and _Case #3_.

**_The student must keep in mind that once they accept the quota, they agree to participate in the event. If the student has doubts, he or she should consider giving the opportunity to other students._**

## Document format

The excel document with the data for compute the ranking must have the following format:

| Code | Name | Cuscontest Position | Codeforces Handle | Team | Category |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 204321 | Yishar Piero Nieto Barrientos | 1 | theFixer | Pancito | Advanced |
| 231442 | Yamir Wagner Florez Vega | 1 | WagnerYFV | Net team  | Intermediate |
| 215733 | Jhon Efrain Quispe Chura | 1 | zero_speed | Null | Beginner |

## Configuration File

`Config` file contains information about:

- Document columns format
- Weights assigned to each tupe of information
- Information on the number of teams participating in the Cuscotest


## Install dependencies

Install dependencies from the `requirements.txt` file with the following command:

```bash
pip install -r requirements.txt
```

## Command to run

To run the script, it is necessary the path to the excel document that is sent through the `filepah` parameter. 

In this sense, the command to execute the script is the following:

``` bash
 python3 ranking.py [filepath]
```
