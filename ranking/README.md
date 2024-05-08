## Compute Ranking

This script compute the **ranking per student** using three specific information which are:

- Position of the **Selective Contest** (70 pts)
- Number of problems solved in codeforces (20 pts)
- Codeforces rating (10 pts)

Additional for each information is considered a **weight** that can be edited in the config file.

### Selective Contest Position Score

For each student `s`, this score consider the position in the **Selective Contest**:

```math
ContestPositionScore_s = \left( { TotalContestTeams - ConstestPosition_s + 1 \over TotalContestTeams }  \right) \left( ContestPositionWeight \right)
```

### Codeforces Rating Score

If `n` students are participating in the selection. For each student `s`, this score will be the **Codeforces rating information obtained by the student in the different online contests**.

The **minimum rating considered is 800**, that is, anyone who has **less than this rating by default will have 800**. 

```math
MaximumCodeforcesRating = \max_{1 \leq s \leq n} \left( CodeforcesRating_s \right)
```

```math
CodeforcesRatingScore_s = \left( { \max \left( 800, CodeforcesRating_s \right)  \over MaximumCodeforcesRating }  \right) \left( CodeforcesRatingWeight \right)
```

### Codeforces Solved Problems Score

If `n` students are participating in the selection and a student solved `p` problems in Codeforces. 

For each student `s`, this score will be computed considering the number of problems solved and the rating of each problem i.e **hard problems give more points than easy problems**

Those **Gym problems that were solved during the training contest due to not having a rating will be considered the rating of 1000 points**.

```math
TotalRatingSolvedProblem_s = \sum_{k=1}^p RatingSolvedProblem_k 
```

```math
MaximumTotalRatingSolvedProblem = \max_{1 \leq s \leq n} \left( TotalRatingSolvedProblem_s \right)
```

```math
RatingSolvedProblemScore_s = \left( {TotalRatingSolvedProblem_s \over MaximumTotalRatingSolvedProblem }  \right) \left( TotalRatingSolvedProblemWeight \right)
```

### Total Points

For each student `s`, the total amount of points is simply the **sum of the points** mentioned above:

```math
TotalScore_s = ContestPositionScore_s + CodeforcesRatingScore_s + RatingSolvedProblemScore_s
```

## Selection Rules

For selection, students have to take into account the following `requirements`:

1. The student must **keep in mind that he or she will miss classes** in different courses during the event. Additionally, **upon returning the student must complete all pending assignments and exams** for the course.

2. Financial support will be requested from the university. However, not all event expenses will be covered, the student **must cover the expenses with their own money (transportation tickets, accommodation and food)**.

3. In the case of the student have financial support from the university. **Upon returning, the student must report to the university for the expenses incurred**.

Taking this into account, **8 slots will be available** and will be filled as follows:

- _Category A_: **4 spots** will be filled with students who have **more than 110 accumulated credits** (from the 6th semester forward).

- _Category B_: **3 spots** will be filled with students who have **less than or equal to 110 accumulated credits** (from the 1st semester to the 5th semester).

- _Category W_: **1 spot** will be filled with a **woman student**, the student can be **_Category A_** or **_Category B_**

For each of the categories mentioned above, the selection process will be as follows:

1. The slots will be filled **taking into account the ranking** generated.

2. If a student **does not meet the requirements**, the slot will be **assigned to the next one in the ranking**.

3.  If there are **no more students in the ranking for that category**. The slot will be **assigned for another category** following the order **_Category A_**, **_Category B_** and **_Category W_**. That means that the selection process will be repeated.


**_The student must keep in mind that once they accept the slot, they agree to participate in the event. If the student has doubts, he or she should consider giving the opportunity to other students._**

## Document format

The CSV document with the data for compute the ranking must have the following format:
Id;Name;Contest Position;Codeforces Handle;Credits;Semester;Gender;Join Discord;Discord;Contest Registered

| Id | Name | Gender | Codeforces Handle | Credits | Semester | Contest Registered | Contest Position |
| - | - | - | - | - | - | - | - |
| 204321 | Yishar Piero Nieto Barrientos | Male | theFixer | 175 | 8 | Yes | 1 |
| 215733 | Jhon Efrain Quispe Chura | Male | zero_speed | 26 | 2 | Yes | 2 |

## Configuration File

`Config` file contains information about:

- Document columns format
- Weights assigned to each type of information
- Information on the number of teams participating in the Cuscotest

## Install dependencies

Install dependencies from the `requirements.txt` file with the following command:

```bash
pip install -r requirements.txt
```

## Command to run

To run the script, it is necessary the path to the CSV document that is sent through the `filepah` parameter.

In this sense, the command to execute the script is the following:

``` bash
pyhton3 ranking.py [data-file-path] [ranking-file-path]

# Example:
python3 ranking.py selections/training-camp-argentina-2024/registered.csv selections/training-camp-argentina-2024
```
