from random import randint
from time import time 

import json
from flask import Flask, render_template, request, jsonify, make_response



app = Flask(__name__) 


answers = {}
# answers =  {cookie: {"answer": answer, "expiration": time + 600}}


# upon a request sent back to the server for ending check or getting a new maze, check for any redundant cookies
def checkExpiry(answerDict):
    for x in answerDict:
        if answerDict[x]["expiration"] < time.time:
            answerDict.pop(x)


def createPerfectMaze(rows, cols):
    # 0 denotes a wall, 1 denotes a path
    curPath = []
    curExit = []

    # # path and pathList acts as a stack, with pathList capturing all the possible paths to every point in the maze from the starting point
    path = []
    pathLength = 0 
    curPathLength = 0

    # creates a blank state of dimensions ( rows + 1 )  * ( cols + 1 )
    curPath.clear()
    mazeMap = [[3 for i in range(cols  + 2)] for j in range(rows + 2)]
    for row in range(rows + 2):
        for col in range(cols + 2):
            if row == 0 or row  == rows + 1 or col == 0  or col == cols + 1:
                mazeMap[row][col] = 2

    # choose a random starting point of (x,y)
    startingCoords = [randint(1, cols), randint(1, rows)]
    # startingCoords = [2,4]


    # choosePath here starts a recursive call to generate the path until further pathing cannot be acheived 

    def choosePath(curCoords):
        # checks validity of path, if alr chosen, out of bounds or has > 2 paths adj, it is invalid
        def checkValid(curCoords):
            ls = []
            counter = 0
            nonlocal curExit
            if mazeMap[curCoords[1]][curCoords[0]] == 2 or mazeMap[curCoords[1]][curCoords[0]] == 1: 
                # if the suggested coord is an outer wall ( 2 ), instantly refuse it
                return False
            # reads and takes down the surroundings around the suggested block
            ls.append(mazeMap[curCoords[1]] [curCoords[0] + 1])
            ls.append(mazeMap[curCoords[1]] [curCoords[0] - 1])
            ls.append(mazeMap[curCoords[1] - 1] [curCoords[0]])
            ls.append(mazeMap[curCoords[1] + 1] [curCoords[0]])
            for cell in ls:
                if cell == 1: 
                    counter += 1
            if counter < 2:
                return True
            return False
        
        if checkValid(curCoords):
            # make it a path
            nonlocal path
            nonlocal pathLength
            nonlocal curPathLength
            nonlocal curExit
            # pt is added to path, path length increases
            pathLength = pathLength + 1
            # check for longer than current longest path
            if pathLength > curPathLength:
                curPathLength = pathLength
                curExit = [curCoords[0], curCoords[1]]
            # assign each location, a pathing route from the starting pt
                curPath.append(path.copy()) 
            # makes the valid location a valid path in the maze
            mazeMap[curCoords[1]][curCoords[0]] = 1
            dirs = [0, 1, 2, 3]
            dir = randint(0,3)
            j = 3
            # first chosen = direction is random, corresponding ones are also 
            for i in range(4):
                if j != 0:
                    j = j -1 
                if dirs[dir] == 0: # y coord + 1, check validity of path, up ( refer to why curCoord[1] - 1 at dir == 2) 
                    path.append([curCoords[0], curCoords[1] - 1]) # add to the running path the chosen dir
                    choosePath([curCoords[0], curCoords[1] - 1])
                    path.pop() # removes from running path after leaving that dir
                    dirs.pop(dir)
                    dir = randint(0, j)
                    continue
                elif dirs[dir]  == 1 : # x + 1, right
                    path.append([curCoords[0] + 1, curCoords[1]])
                    choosePath([curCoords[0] + 1, curCoords[1]])
                    path.pop()
                    dirs.pop(dir)
                    dir = randint(0, j)
                    continue
                elif dirs[dir]  == 2: # y - 1, down ( + 1 to curCoords[1] due to y axis increasing downwards)
                    path.append([curCoords[0], curCoords[1] + 1])
                    choosePath([curCoords[0], curCoords[1] + 1])
                    path.pop()
                    dirs.pop(dir)
                    dir = randint(0, j)
                    continue
                elif dirs[dir]  == 3: # x - 1, left
                    path.append([curCoords[0] - 1, curCoords[1]])
                    choosePath([curCoords[0] - 1, curCoords[1]])
                    path.pop()
                    dirs.pop(dir)
                    dir = randint(0, j)
                    continue  
                else:
                    print("ERROR")
                    return
            pathLength = pathLength - 1
        else:
            return True
   
    path.append(startingCoords)
    choosePath(startingCoords)
    # sets exit pt
    mazeMap[curExit[1]] [curExit[0]] = 1
    # sets start pt 
    mazeMap[startingCoords[1]] [startingCoords[0]] = 1

    for row in mazeMap:
        print(row)
    # prints the latest added new location(which is the exit)-> can consider iterating thru the list to find the longest path too
    print(curPath[-1])
    ls = startingCoords.copy()
    ls.extend(curExit)
    ls.extend(mazeMap)
    ls.append(curPath[-1])
    
    return ls
    


def checkPath(curCoords, mazeMap, curPath):
    # coords to be in the form [x,y]
    # checks the adj points for possible path and returns the list of possible path in a list with their coords in it
    choosingList = []
    def checkPoint(yCoords,xCoords):
        nonlocal choosingList
        if mazeMap[yCoords][xCoords] == 1 and [xCoords,yCoords] != curPath[0]:
            choosingList.append([xCoords,yCoords])
    checkPoint(curCoords[1], curCoords[0] + 1)
    checkPoint(curCoords[1], curCoords[0] - 1)
    checkPoint(curCoords[1] - 1, curCoords[0])
    checkPoint(curCoords[1] + 1, curCoords[0])
    print(choosingList)
    return choosingList

    

@app.route("/", methods=['POST', 'GET'])
def index():
    startEnd = []
    if request.method == 'POST':
        
        coords = request.get_json()
        if coords == "new map":
            print("sending new maze")
            startEnd = createPerfectMaze(10,10)
            mazeMap = startEnd[4:len(startEnd)-1]
            curPath = startEnd[len(startEnd) - 1]
            choosingList = json.dumps(checkPath(curPath[0],mazeMap,curPath))
            ls = [mazeMap, choosingList, startEnd[:2], startEnd[2:4]]
            
            if answers.pop(request.cookies.get("curMaze"), None) is None:
                print("no cookie found")
                # currently js sends them a new maze with a new cookie
            print(answers)
            resp = make_response(jsonify(ls))
            key = json.dumps(mazeMap)
            resp.set_cookie("curMaze", key, max_age=600) # sets in the cookie directory, the maze map 
            answers.update({f"{key}" :{"answer" : f"{curPath}", "expiration" : time.time() + 600} })
            return resp
            # check if coords == pathList
        print("ending check")
        if request.cookies.get("curMaze", "no cookie") is "no cookie":
            # cookie cannot be found-> reload page
            print("no cookie found")
            # check for expried cookies and remove any
            checkExpiry(answers)
            return jsonify(True)
        i = 0
        answer = True
        curAnswer = json.loads(answers.get(request.cookies.get("curMaze")).get("answer")) 
        checkExpiry(answers)
        # reads the cookies to get the maze, then looks in the dict for the corresponding answer
        print(curAnswer)
        
        for data in coords:
            print(data)
            if data != curAnswer[i]:
                answer = False
                return jsonify(False)
            i += 1
            print(i)
        if i == len(curAnswer) - 1: 
            return jsonify(answer)
        else:
            return jsonify(False)

        # check if user has completed the maze, the coords sent back is the ending one -> clear path and generate new maze
        # else check new path
    elif request.method == 'GET':
        startEnd = createPerfectMaze(10,10)
        mazeMap = startEnd[4:len(startEnd) - 1]
        curPath = startEnd[len(startEnd) - 1]

        choosingList = json.dumps(checkPath(curPath[0], mazeMap,curPath))   # returns the list of possible paths
    # curPath shld only be cleared once the indiv has finished the curMaze
        resp = make_response(render_template("index.html", mazeMap=mazeMap, choosingList=choosingList, startingCoords=startEnd[:2], endingCoords=startEnd[2:4]))
        key = json.dumps(mazeMap)
        
        resp.set_cookie("curMaze", key, max_age=600) # sets in the cookie directory, the maze map 
        answers.update({f"{key}" :{"answer" : f"{curPath}", "expiration" : time.time() + 600} })
        #  this stores the maze map as the key, and a dict containing the answer and the cookie expiration time as a key-value pair
        print(answers)
        checkExpiry(answers)
        return resp

#TODO:

# 1. expiration of cookie -> set up a read of the dict, to get which answers/cookies have expired + set the cookie to expire (in 10 mins)
# 2. error handling of no key found
# 3. removal of the global variables-> transit to cookies (need to update the dict to add in expiration time)
