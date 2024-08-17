import os
import json
from datetime import datetime

metadataDir = "metadata"
problemsFile = "problems.json"
submissionsFile = "submissions.json"
runsFile = "runs.json"
contestantsFile = "accounts.json"
unfrozenFile = "unfrozen.json"

hashVeredict = {
    "AC" : "Accepted", 
    "WA" : "Wrong Answer",
    "TLE" : "Wrong Answer",
    "MLE" : "Wrong Answer",
    "OLE" : "Wrong Answer",
    "RTE" : "Wrong Answer",
    "NO" : "Wrong Answer",
    "CE" : "Compilation Error" 
}

verdicts = {
    "accepted": ["Accepted"],
    "wrongAnswerWithPenalty": ["Wrong answer"],
    "wrongAnswerWithoutPenalty": ["Compilation error"]
}

class ContestMetadata:
    duration = 0
    frozenTimeDuration = 0
    name = ""
    type = ""

    def __init__(self, duration, frozenTimeDuration, name, type):
        self.duration = duration
        self.frozenTimeDuration = frozenTimeDuration
        self.name = name
        self.type = type

class Problem:
    index = ""  
    def __init__(self, index):
        self.index = index


class Contestant:
    id = 0
    name = ""

    def __init__(self, id, name):
        self.id = id
        self.name = name

class Submission:
    timeSubmitted = 0
    contestantName = ""
    problemIndex = ""
    verdict = ""

    def __init__(self, timeSubmitted, contestantName, problemIndex, verdict):
        self.timeSubmitted = timeSubmitted
        self.contestantName = contestantName
        self.problemIndex = problemIndex
        self.verdict = verdict

def readJsonFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as stream:
        data = json.load(stream)
    return data

def writeJsonFile(data):
    filepath = os.path.join(metadataDir, unfrozenFile)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


def getContestMetadata():
    contestMetadata = ContestMetadata(300, 60, "Cuscontest XXI", "ICPC")
    return contestMetadata.__dict__

def getProblems():
    filepath = os.path.join(metadataDir, problemsFile)
    problemsJson = readJsonFile(filepath)
    problems = []
    problemsById = {}
    for problem in problemsJson:
        index = problem["short_name"]
        problemId = problem["id"]
        problems.append(Problem(index))
        problemsById[problemId] = index

    return [p.__dict__ for p in problems], problemsById

def getContestants():
    filepath = os.path.join(metadataDir, contestantsFile)
    contestantsJson = readJsonFile(filepath)
    contestants = []
    teamsById = {}
    for team in contestantsJson:
        id = int(team["id"])
        name = team["team"]
        if name is None:
            continue
        teamsById[id] = name
        contestants.append(Contestant(id, name))

    return [c.__dict__ for c in contestants], teamsById


def getVeredicts(runsByJudgementId):
    veredictsByJudgementId = {}
    for run in runsByJudgementId:
        verdict = run["judgement_type_id"]
        if verdict not in veredictsByJudgementId:
            veredictsByJudgementId[verdict] = 0
        veredictsByJudgementId[verdict] += 1

    return veredictsByJudgementId


def getFinalVeredict(veredicts):
    if len(veredicts) == 1:
        return hashVeredict[next(iter(veredicts))]
    return hashVeredict["WA"]


def getRuns():
    filespathRuns = os.path.join(metadataDir, runsFile)
    runsJson = readJsonFile(filespathRuns)

    runsById = {}

    for run in runsJson:
        judgementId = run["judgement_id"]
        if judgementId not in runsById:
            runsById[judgementId] = []
        runsById[judgementId].append(run)
    
    return runsById


def getSubmissions(teamsById, problemsById):
    filepathSubmissions = os.path.join(metadataDir, submissionsFile)
    submissionsJson = readJsonFile(filepathSubmissions)

    runsById = getRuns()
    submissions = []

    for submission in submissionsJson:
        contestTime = submission["contest_time"]
        problemId = submission["problem_id"]
        teamId = int(submission["team_id"])
        submissionId = submission["id"]

        if submissionId not in runsById:
            continue

        time = datetime.strptime(contestTime, "%H:%M:%S.%f")
        hours = time.hour
        minutes = time.minute
        timeSubmitted = hours*60 + minutes

        contestantName = teamsById[teamId]
        
        problemIndex = problemsById[problemId]

        
        veredicts = getVeredicts(runsById[submissionId])
        verdict = getFinalVeredict(veredicts)

        submissions.append(Submission(timeSubmitted, contestantName, problemIndex, verdict))

    return [s.__dict__ for s in submissions]



#  MAIN FUNCTION

def unfrozeScoreboard():
    contestMetadata = getContestMetadata()
    problems, problemsById = getProblems()
    contestants, teamsById = getContestants()
    submissions = getSubmissions(teamsById, problemsById)
    scoreboardJson = {
        "contestMetadata" : contestMetadata,
        "problems" : problems, 
        "contestants" : contestants,
        "verdicts" : verdicts,
        "submissions" : submissions,

    }
    writeJsonFile(scoreboardJson)

    #print(json.dumps(scoreboardJson, indent = 4))

def main():
    scoreboardJson = unfrozeScoreboard()

main()