## Compute Scoreboard

This script compute the **contest scoreboard** using CSV file

## Document format

The CSV document with the data for compute the scoreboard must have the following format:

- `1` : Solved Problem
- `-1` : Failed attempt
- `0` : Unsolved Problem

| Id | Name | Codeforces Handle | Penalty | A | B | C |
| - | - | - | - | - | - | - |
| 204321 | Yishar Piero Nieto Barrientos | theFixer | 26 | 1 | 1 | 1 |
| 231447 | Rosy Aurely Montalvo Solórzano | LittleProgramer4 | 28 | 1 | 1 | -1 |
| 215733 | Jhon Efrain Quispe Chura | zero_speed | 30 | 1 | -1 | 0 |

## Configuration File

`Config` file contains information about:

- Document columns format
- Document column problems
- Number of problems

## Install dependencies

Install dependencies from the `requirements.txt` file with the following command:

```bash
pip install -r requirements.txt
```

## Command to run

To run the script, it is necessary the path to the CSV document that is sent through the `filepah` parameter.

In this sense, the command to execute the script is the following:

``` bash
pyhton3 scoreboard.py [data-file-path] [output-file-path] [config-file-path]

# Example:
python3 scoreboard.py selection/training-camp-argentina-2024/scoreboard.csv selection/training-camp-argentina-2024 Config
```
