import requests
import json
import openpyxl
import sys
import configparser
from tabulate import tabulate

class User:
    # Basic information
    id = ""
    name = ""
    position = 0
    handle = ""
    category = ""

    # Codeforces information
    ratingUser = 0
    ratingProblems = 0

    # Compute points
    positionPoints = 0.0
    ratingPoints = 0.0
    problemPoints = 0.0
    totalPoints = 0.0

    def __init__(self, id, name, position, handle, category):
        self.id = id
        self.name = name
        self.handle = handle
        self.position = position
        self.category = category

        print('Loading Codeforces info for \"{0}\" with handle \"{1}\"'.format(self.name, self.handle))
        self.getUserRating()
        self.getSolvedProblemsRating()
        print("Loading basic information for \"{0}\"".format(self.name))


    def getUserRating(self):
        link = f"https://codeforces.com/api/user.info?handles={self.handle}"
        url = requests.get(link)
        data = json.loads(url.text)

        if 'rating' in data["result"][0].keys():
            self.ratingUser = data["result"][0]["rating"]

        # Minimum rating is 800
        self.ratingUser = max(800, self.ratingUser)


    def getSolvedProblemsRating(self):
        link = f"https://codeforces.com/api/user.status?handle={self.handle}"
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
                self.ratingProblems  += submissions["problem"]["rating"]  
                problemSolved[key] = True

            # Training contest problems have 1000 of raiting
            if  key not in problemSolved and "rating" not in submissions["problem"]:
                self.ratingProblems += 1000
                problemSolved[key] = True


class Ranking:
    config = {}
    users = []

    totalUsers = 0
    totalTeams = 0

    ratingUserAverage = 0
    ratingProblemsAverage = 0
    maxRatingUser = 0
    maxRatingProblems = 0

    positionWeight = 0
    ratingWeight = 0
    problemsWeight = 0

    def __init__(self, config, users):
        self.config = config
        self.users = users
        self.totalUsers = len(users)
        
        print("Computing ranking...")
        self.computeRanking()
        print("Completed computing the ranking!")

    def computeRanking(self):
        ratingUserAccumulate = 0
        ratingProblemsAccumulate = 0

        for user in self.users:
            ratingUserAccumulate += user.ratingUser
            ratingProblemsAccumulate += user.ratingProblems
            self.maxRatingUser = max(self.maxRatingUser, user.ratingUser)
            self.maxRatingProblems = max(self.maxRatingProblems, user.ratingProblems)

        self.ratingUserAverage = ratingUserAccumulate / self.totalUsers
        self.ratingProblemsAverage = ratingProblemsAccumulate / self.totalUsers

        self.totalTeams = int(self.config["Contest"]["TotalTeams"])

        self.positionWeight = int(self.config["Weight"]["Position"])
        self.ratingWeight = int(self.config["Weight"]["Rating"])
        self.problemsWeight = int(self.config["Weight"]["Problems"])

        for user in self.users:  
            user.positionPoints = (self.totalTeams - user.position + 1) * self.positionWeight / self.totalTeams 
            user.ratingPoints = (user.ratingUser / self.maxRatingUser) * self.ratingWeight
            user.problemsPoints = (user.ratingProblems / self.maxRatingProblems) * self.problemsWeight
            user.totalPoints = user.positionPoints + user.ratingPoints + user.problemsPoints

        self.users.sort(key = lambda user : user.totalPoints, reverse = True)

    def plotTable(self):
        headers = ["#", "Id", "Name", "Handle", "Category", "Position" , "Rating", "Problems", "Contest Points", "Rating Points", "Problem Points" ,"Total Score"]
        
        table = []
        position = 1
        for user in self.users:
            table.append([position, user.id, user.name, user.handle, user.category, user.position , user.ratingUser, user.ratingProblems, user.positionPoints, user.ratingPoints, user.problemsPoints, user.totalPoints])
            position += 1

        rankingTable = tabulate(table, headers=headers, tablefmt='orgtbl')
        print("Ranking completed!")
        print("")
        print("Contest Position Weight: {0}".format(self.positionWeight))
        print("Codeforces Rating Weight: {0}".format(self.ratingWeight))
        print("Codeforces Accumulate Problem Rating Weight: {0}".format(self.problemsWeight))
        print("")
        print("Total Contest Teams: {0}".format(self.totalTeams))
        print("")
        print("Total participants in the selection: {0}".format(self.totalUsers))
        print("Maximum rating of the participants in the selection: {0}".format(self.maxRatingUser))
        print("Maximum accumulated problem rating of the participants in the selection: {0}".format(self.maxRatingProblems))
        print("Average rating of the participants in the selection: {0}".format(self.ratingUserAverage))
        print("Average of the accumulated problem rating of the participants in the selection: {0}".format(self.ratingProblemsAverage))
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
    dataframe = openpyxl.load_workbook(filepath)
    data = dataframe.active
    print("File reading is completed!")
    return data

def getUsers(config, data):
    idCol = int(config["Column"]["Id"])
    nameCol = int(config["Column"]["Name"])
    positionCol = int(config["Column"]["Position"])
    handleCol = int(config["Column"]["Handle"])
    categoryCol = int(config["Column"]["Category"])

    print("Loading users information...")
    users = []
    for row in range(2, data.max_row + 1):
        id = data.cell(row, idCol).value
        name = data.cell(row, nameCol).value
        position = data.cell(row, positionCol).value
        handle = data.cell(row, handleCol).value
        category = data.cell(row, categoryCol).value

        if id == None or name == None or handle == None or category == None:
            continue

        user = User(id, name, position, handle, category)
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
