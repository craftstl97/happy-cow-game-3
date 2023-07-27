# Homework 3
# Puzzle3.py
# Christian Craft

import random
import sys
import fileinput

# python library to handle heaps
import heapq

# AI places cows determined by Iterative Deepening
def placeCowsID(grid: list, gridSize: int):
    # set to True to break the anticipation of execution
    feedback = False
    frontier = []
    populateFrontier(frontier, [], grid, gridSize)
    # pop -1 for FILO (DFS)
    currentNode = frontier.pop(-1)
    bestScore = 0
    iterations = 0
    depthLimit = 0
    depthHit = False
    # goal score of 7 should be possible with a maximum of 7 cows
    while currentNode[0] < 7 and len(currentNode[1]) < 8:
        # ignore previously visited paths
        # populate the frontier if the depth limit isn't reached
        if len(currentNode[1]) <= depthLimit:
            populateFrontier(frontier, currentNode[1], grid, gridSize)

        # pop 0 for FIFO (BFS), -1 for FILO (DFS)
        currentNode = frontier.pop(-1)
        if len(frontier) == 0:
            # restore the root when frontier is empty
            populateFrontier(frontier, [], grid, gridSize)
            depthLimit += 1
        iterations += 1
        if currentNode[0] > bestScore and feedback:
            bestScore = currentNode[0]
            print("New best score of", bestScore, "at", iterations, "iterations")
            print(currentNode)
    if len(currentNode[1]) >= 7 and feedback:
        print("Depth limit reached after", iterations, "iterations")
    placeCows(currentNode[1], grid)

# Adds all leaf nodes to the frontier
def populateFrontier(frontier: list, parentNode: list, grid: list, gridSize: int):
    # iterate through grid
    # push all possible cow placements and their scores to the frontier
    offX = 0
    offY = 0
    tempNode = parentNode

    # ignore duplicate entries
    if len(parentNode):
        offX = parentNode[-1][0]
        offY = parentNode[-1][1]

    # place cows to ensure no duplicates
    placeCows(tempNode, grid)
    for x in range(gridSize - offX):
        for y in range(gridSize - offY):
            # if the tile is grass
            if grid[x + offX][y + offY] == ".":
                # temporarily make it a cow and place all other cows
                line = list(grid[x + offX])
                line[y + offY] = "C"
                grid[x + offX] = "".join(line)

                # score and push the temp placement
                tempScore = scorePlacement(grid, gridSize)
                tempNode.append((x + offX, y + offY))

                frontier.append((tempScore, tempNode[:]))
                tempNode.pop()

                line = list(grid[x + offX])
                line[y + offY] = "."
                grid[x + offX] = "".join(line)

        # offY is not longer needed after the first loop
        offY = 0
    # remove all placed cows
    removeCows(tempNode, grid)

# handles command line input
def getFileNames(argv):
    iFile = argv[0]
    oFile = argv[1]

    return (iFile, oFile)


# checks if a given row col pair is in the grid
def inRange(row: int, col: int, gridSize: int) -> bool:
    if row < 0 or col < 0 or row > gridSize - 1 or col > gridSize - 1:
        return False
    return True


# checks adjacent spaces for cows, haystacks, and ponds
def setFlags(row: int, col: int, grid: list, gridSize: int) -> tuple:
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
    cow = False
    hay = False
    pond = False

    # iterate through offsets
    for dir in range(8):
        testRow = row + offsets[dir][0]
        testCol = col + offsets[dir][1]
        if inRange(testRow, testCol, gridSize):
            # check all spaces for cows
            if grid[testRow][testCol] == "C":
                cow = True

            # don't check corners for hay or ponds
            if dir % 2 == 1:
                if grid[testRow][testCol] == "@":
                    hay = True
                if grid[testRow][testCol] == "#":
                    pond = True

        # return if all flags are set
        if cow and hay and pond:
            return (cow, hay, pond)

    # otherwise return all flags when done
    return (cow, hay, pond)


def scoreCow(x: int, y: int, grid: list):
    # flags to identify adjacent tiles
    haystack = False
    pond = False
    cow = False
    cowScore = 0

    # check the surrounding tiles and update flags
    flags = setFlags(x, y, grid, gridSize)
    cow = flags[0]
    haystack = flags[1]
    pond = flags[2]

    # haystack = +1
    if haystack:
        cowScore += 1
        # haystack and pond = +3
        if pond:
            cowScore += 2
    # cow = -3
    if cow:
        cowScore -= 3

    return cowScore


# returns the score of a given placement
def scorePlacement(grid: list, gridSize: int) -> int:
    cowScore = 0
    totalScore = 0
    # iterate through the entire grid
    for x in range(gridSize):
        for y in range(gridSize):
            # check for cow
            if grid[x][y] == "C":
                totalScore += scoreCow(x, y, grid)

    return totalScore


# takes a list of (x,y) coordinates and places cows in the grid
def placeCows(coordinates: list, grid: list):
    for element in coordinates:
        line = list(grid[element[0]])
        line[element[1]] = "C"
        grid[element[0]] = "".join(line)


# takes a list of (x,y) coordinates and removes cows in the grid
def removeCows(coordinates: list, grid: list):
    for element in coordinates:
        line = list(grid[element[0]])
        line[element[1]] = "."
        grid[element[0]] = "".join(line)

# AI places cows determined by Iterative Deepening
def placeCowsID(grid: list, gridSize: int):
    # set to True to break the anticipation of execution
    feedback = False
    frontier = []
    populateFrontier(frontier, [], grid, gridSize)
    # pop -1 for FILO (DFS)
    currentNode = frontier.pop(-1)
    bestScore = 0
    iterations = 0
    depthLimit = 0
    depthHit = False
    # goal score of 7 should be possible with a maximum of 7 cows
    while currentNode[0] < 7 and len(currentNode[1]) < 8:
        # ignore previously visited paths
        # populate the frontier if the depth limit isn't reached
        if len(currentNode[1]) <= depthLimit:
            populateFrontier(frontier, currentNode[1], grid, gridSize)

        # pop 0 for FIFO (BFS), -1 for FILO (DFS)
        currentNode = frontier.pop(-1)
        if len(frontier) == 0:
            # restore the root when frontier is empty
            populateFrontier(frontier, [], grid, gridSize)
            depthLimit += 1
        iterations += 1
        if currentNode[0] > bestScore and feedback:
            bestScore = currentNode[0]
            print("New best score of", bestScore, "at", iterations, "iterations")
            print(currentNode)
    if len(currentNode[1]) >= 7 and feedback:
        print("Depth limit reached after", iterations, "iterations")
    placeCows(currentNode[1], grid)


# writes to output file
def writeToFile(fileName: str, gridSize: int, grid: list):
    file = open(fileName, "w")
    # grid size
    file.write(str(gridSize) + "\n")

    # grid
    for line in grid:
        file.write(line + "\n")

    # Score
    file.write(str(scorePlacement(grid, gridSize)))
    file.close()


# main driver function
if __name__ == "__main__":
    grid = []
    IO = getFileNames(sys.argv[1:])

    for line in fileinput.input(files=IO[0]):
        grid.append(line.strip())

    # removes the grid size line and stores it as an integer
    gridSize = int(grid.pop(0))

    # counts the haystacks
    haystacks = 0
    for line in grid:
        for placement in line:
            if placement == "@":
                haystacks += 1

    # place one cow for every haystack
    # for x in range(haystacks):
    # placeCowRand(grid, gridSize)

    # place cows until score is at least 7
    placeCowsID(grid, gridSize)

    # write the grid size, grid, and score to the file
    writeToFile(IO[1], gridSize, grid)
