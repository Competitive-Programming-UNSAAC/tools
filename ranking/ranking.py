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
    totalTeamsBeginner = 0
    totalTeamsIntermediate = 0
    ratingUserAverage = 0
    ratingProblemsAverage = 0

    def __init__(self, config, users):
        self.config = config
        self.users = users
        self.totalUsers = len(users)
        
        print("Computing ranking...")
        self.computeRanking()
        print("Completed computing the ranking!")

    def computeRanking(self):
        ratingAccumulate = 0
        ratingProblemsAccumulate = 0
        maxRating = 0
        maxProblems = 0

        for user in self.users:
            ratingAccumulate += user.ratingUser
            ratingProblemsAccumulate += user.ratingProblems
            maxRating = max(maxRating, user.ratingUser)
            maxProblems = max(maxProblems, user.ratingProblems)

        self.ratingUserAverage = ratingAccumulate / self.totalUsers
        self.ratingProblemsAverage = ratingProblemsAccumulate / self.totalUsers

        self.totalTeams = int(self.config["Contest"]["TotalTeams"])
        self.totalTeamsBeginner = int(self.config["Contest"]["TotalTeamsBeginner"])
        self.totalTeamsIntermediate = int(self.config["Contest"]["TotalTeamsIntermediate"])

        positionWeight = int(self.config["Weight"]["Position"])
        ratingWeight = int(self.config["Weight"]["Rating"])
        problemsWeight = int(self.config["Weight"]["Problems"])

        totalTeamsByCategory = 0
        for user in self.users:
            if user.category == "Beginner":
                totalTeamsByCategory = self.totalTeamsBeginner
            else:
                totalTeamsByCategory = self.totalTeamsIntermediate
            
            user.positionPoints = (totalTeamsByCategory - user.position + 1) * positionWeight / totalTeamsByCategory
            user.ratingPoints = (user.ratingUser / maxRating) * ratingWeight
            user.problemsPoints = (user.ratingProblems / maxProblems) * problemsWeight
            user.totalPoints = user.positionPoints + user.ratingPoints + user.problemsPoints

        self.users.sort(key = lambda user : user.totalPoints, reverse = True)

    def plotTable(self):
        headers = ["#", "Id", "Name", "Handle", "Rating", "Problems", "Cuscontest XX", "Rating Points", "Problem Points" ,"Total Score"]
        
        table = []
        position = 1
        for user in self.users:
            table.append([position, user.id, user.name, user.handle, user.ratingUser, user.ratingProblems, user.positionPoints, user.ratingPoints, user.problemsPoints, user.totalPoints])
            position += 1

        rankingTable = tabulate(table, headers=headers, tablefmt='orgtbl')
        print("Ranking completed!")
        print("")
        print("Total teams: {0}".format(self.totalTeams))
        print("Total beginner teams: {0}".format(self.totalTeamsBeginner))
        print("Total intermediate teams: {0}".format(self.totalTeamsIntermediate))
        print("Total selection participants: {0}".format(self.totalUsers))
        print("Average rating of participants: {0}".format(self.ratingUserAverage))
        print("Average sum of difficulty of problem solved of participants: {0}".format(self.ratingProblemsAverage))
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

def getUsers(data, config):
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

        if id == None or name == None or handle == None:
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

    users = getUsers(data, config)
    ranking = Ranking(config, users)

    ranking.plotTable()

main()
