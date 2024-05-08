import sys
import json
import requests
import openpyxl
import csv
import configparser
from tabulate import tabulate

class User:
    # Basic information
    id = ""
    name = ""
    gender = ""
    codeforcesHandle = ""
    credits = 0
    contestRegistered = ""
    contestPosition = 0

    # Contest
    isRegisteredOnContest = False

    # Category
    category = ""

    # Codeforces information
    codeforcesRating = 0
    totalRatingSolvedProblems = 0

    # Compute scores
    contestPositionScore = 0.0
    codeforcesRatingScore = 0.0
    ratingSolvedProblemScore = 0.0
    totalScore = 0.0

    def __init__(self, id, name, gender, codeforcesHandle, credits, contestRegistered , contestPosition):
        self.id = id
        self.name = name
        self.gender = gender
        self.codeforcesHandle = codeforcesHandle
        self.credits = int(credits)
        self.contestRegistered = contestRegistered
        self.contestPosition = int(contestPosition)

        print('Loading Codeforces info for \"{0}\" with handle \"{1}\"'.format(self.name, self.codeforcesHandle))
        self.getCodeforcesRating()
        self.getTotalRatingSolvedProblems()
        self.isRegisteredOnContest()
        print("Loading basic information for \"{0}\"".format(self.name))

    def isRegisteredOnContest(self):
        if self.contestRegistered == "Yes":
            self.isRegisteredOnContest = True

    def getCodeforcesRating(self):
        link = f"https://codeforces.com/api/user.info?handles={self.codeforcesHandle}"
        url = requests.get(link)
        data = json.loads(url.text)

        if 'rating' in data["result"][0].keys():
            self.codeforcesRating = data["result"][0]["rating"]

        # Minimum rating is 800
        self.codeforcesRating = max(800, self.codeforcesRating)


    def getTotalRatingSolvedProblems(self):
        link = f"https://codeforces.com/api/user.status?handle={self.codeforcesHandle}"
        url = requests.get(link)
        data = json.loads(url.text)

        problemSolved = {}
        for submissions in data["result"]:
            # Prepare id for the problem
            key = ""
            if 'problemsetName' in submissions["problem"].keys():
                key += submissions["problem"]["problemsetName"]

            if 'contestId' in submissions["problem"].keys():
                key += str(submissions["problem"]["contestId"])

            if 'index' in submissions["problem"].keys():
                key += submissions["problem"]["index"]    

            # Accumulate problem rating avoid duplicates
            if  key not in problemSolved and submissions['verdict'] == "OK" and "rating" in submissions["problem"]:      
                self.totalRatingSolvedProblems  += submissions["problem"]["rating"]
                problemSolved[key] = True

            # Training contest problems have 1000 of raiting
            if  key not in problemSolved and "rating" not in submissions["problem"]:
                self.totalRatingSolvedProblems += 1000
                problemSolved[key] = True


class Ranking:
    config = {}
    users = []

    totalUsers = 0
    totalRegisteredTeams = 0
    totalContestTeams = 0

    creditsThreshold = 0

    codeforcesRatingAverage = 0.0
    totalRatingSolvedProblemsAverage = 0.0
    maximumCodeforcesRating = 0
    maximumTotalRatingSolvedProblem = 0

    contestPositionWeight = 0
    codeforcesRatingWeight = 0
    totalRatingSolvedProblemsWeight = 0

    def __init__(self, config, users):
        self.config = config
        self.users = users
        self.totalUsers = len(users)
        
        print("Computing ranking...")
        self.computeRanking()
        print("Completed computing the ranking!")

    def getUserCategory(self, user):
        if user.credits > self.creditsThreshold:
            return "A"
        else:
            return "B"

    def getContestPositionScore(self, user):
        return (self.totalContestTeams - user.contestPosition + 1) * self.contestPositionWeight / self.totalContestTeams

    def getCodeforcesRatingScore(self, user):
        return (user.codeforcesRating / self.maximumCodeforcesRating) * self.codeforcesRatingWeight

    def getRatingSolvedProblemScore(self, user):
        return (user.totalRatingSolvedProblems / self.maximumTotalRatingSolvedProblem) * self.totalRatingSolvedProblemsWeight

    def computeRanking(self):
        self.totalRegisteredTeams = int(self.config["Contest"]["TotalRegisteredTeams"])
        self.contestPositionWeight = int(self.config["Weight"]["ContestPosition"])
        self.codeforcesRatingWeight = int(self.config["Weight"]["CodeforcesRating"])
        self.totalRatingSolvedProblemsWeight = int(self.config["Weight"]["TotalRatingSolvedProblems"])
        self.creditsThreshold = int(self.config["Credits"]["Threshold"])

        totalCodeforcesRatingAccumulate = 0
        totalRatingSolvedProblemAccumulate = 0
        for user in self.users:
            totalCodeforcesRatingAccumulate += user.codeforcesRating
            totalRatingSolvedProblemAccumulate += user.totalRatingSolvedProblems
            self.maximumCodeforcesRating = max(self.maximumCodeforcesRating, user.codeforcesRating)
            self.maximumTotalRatingSolvedProblem = max(self.maximumTotalRatingSolvedProblem, user.totalRatingSolvedProblems)

            # Count those registered in the contest
            if user.isRegisteredOnContest:
                self.totalContestTeams += 1

        self.codeforcesRatingAverage = totalCodeforcesRatingAccumulate / self.totalUsers
        self.totalRatingSolvedProblemsAverage = totalRatingSolvedProblemAccumulate / self.totalUsers

        for user in self.users:
            user.category = self.getUserCategory(user)

            user.contestPositionScore = self.getContestPositionScore(user)
            user.codeforcesRatingScore = self.getCodeforcesRatingScore(user)
            user.ratingSolvedProblemScore = self.getRatingSolvedProblemScore(user)

            user.totalScore = user.contestPositionScore + user.codeforcesRatingScore + user.ratingSolvedProblemScore

        # Sort users by total score
        self.users.sort(key = lambda user : user.totalScore, reverse = True)

    def plotTable(self):
        headers = ["#", "Id", "Name", "Gender", "Handle", "Category", "Contest", "Problems", "Rating", "Contest Score", "Problems Score", "Rating Score", "Total Score"]
        
        table = []
        place = 1
        for user in self.users:
            table.append([place, user.id, user.name, user.gender, user.codeforcesHandle, user.category, user.contestPosition , user.totalRatingSolvedProblems, user.codeforcesRating, user.contestPositionScore, user.ratingSolvedProblemScore, user.codeforcesRatingScore, user.totalScore])
            place += 1

        rankingTable = tabulate(table, headers=headers, tablefmt='orgtbl', floatfmt=".2f")

        print("Ranking completed!")
        print("")
        print("Contest Position Weight: {0}".format(self.contestPositionWeight))
        print("Codeforces Total Rating of Solved Problems Weight: {0}".format(self.totalRatingSolvedProblemsWeight))
        print("Codeforces Rating Weight: {0}".format(self.codeforcesRatingWeight))
        print("Total participants in the selection: {0}".format(self.totalUsers))
        print("Total registered teams: {0}".format(self.totalRegisteredTeams))
        print("Total contest teams: {0}".format(self.totalContestTeams))
        print("Maximum Codeforces rating of the participants in the selection: {0}".format(self.maximumCodeforcesRating))
        print("Maximum accumulated problem rating of the participants in the selection: {0}".format(self.maximumTotalRatingSolvedProblem))
        print("Average rating of the participants in the selection: {0}".format(self.codeforcesRatingAverage))
        print("Average of the accumulated problem rating of the participants in the selection: {0}".format(self.totalRatingSolvedProblemsAverage))
        print("")
        print(rankingTable)


def readConfig(filepath):
    print("Reading config from \"{0}\" file...".format(filepath))
    config = configparser.ConfigParser()
    config.read(filepath)
    print("Config reading is completed!")
    return config

def readData(filepath):
    print("Reading data from \"{0}\" file...".format(filepath))
    dataframe = openpyxl.Workbook()
    data = dataframe.active

    with open(filepath) as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
             data.append(row)

    print("File reading is completed!")
    return data

def getUsers(config, data):
    idCol = int(config["Column"]["Id"])
    nameCol = int(config["Column"]["Name"])
    genderCol = int(config["Column"]["Gender"])
    codeforcesHandleCol = int(config["Column"]["CodeforcesHandle"])
    creditsCol = int(config["Column"]["Credits"])
    contestPositionCol = int(config["Column"]["ContestPosition"])
    contestRegisteredCol = int(config["Column"]["ContestRegistered"])

    print("Loading users information...")
    users = []
    for row in range(2, data.max_row + 1):
        id = data.cell(row, idCol).value
        name = data.cell(row, nameCol).value
        gender = data.cell(row, genderCol).value
        codeforcesHandle = data.cell(row, codeforcesHandleCol).value
        credits = data.cell(row, creditsCol).value
        contestPosition = data.cell(row, contestPositionCol).value
        contestRegistered = data.cell(row, contestRegisteredCol).value

        if id == None or name == None or gender == None or codeforcesHandle == None or credits == None or contestPosition == None or contestRegistered == None:
            continue

        user = User(id, name, gender, codeforcesHandle, credits, contestRegistered, contestPosition)
        users.append(user)

    print("Loading users information is completed!")
    return users

def main():
    dataFilepath = sys.argv[1]
    configFilepath = "Config"

    config = readConfig(configFilepath)
    data = readData(dataFilepath)

    users = getUsers(config, data)
    ranking = Ranking(config, users)

    ranking.plotTable()

main()
