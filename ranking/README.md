## Compute Ranking

This script compute the ranking per student using three specific information which are:
- position of the last CUSCONTEST
- Codeforces rating
- Number of problems solved in codeforces

#### Cuscontest Position

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```

When $a \ne 0$, there are two solutions to $(ax^2 + bx + c = 0)$ and they are

```math
x = {-b \pm \sqrt{b^2-4ac} \over 2a}
```

#### Codeforces Ratng

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```

#### Codeforces Solved Problems

```math
\left( \sum_{k=1}^n a_k b_k \right)^2 \leq \left( \sum_{k=1}^n a_k^2 \right) \left( \sum_{k=1}^n b_k^2 \right)
```

## Document format

The excel document with the data for compute the ranking must have the following format:

| Codigo | Nombre | PuestoCuscontest | HandleCodeforces | Equipos | Categoria |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 204321 | Yishar Piero Nieto Barrientos | 1 | theFixer | Pancito | Intermediate |
| 231442 | Yamir Wagner Florez Vega | WagnerYFV | 1 | Net team  | Beginner |

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
