import heapq
import numpy as np
import math
import random
import time
import datetime
import argparse

def getManhattanDistance(fromState, toState, gridSize):
    """
    A function that calculates the Manhattan Distance between all tiles.

    INPUT: 
        Two states
        The size of one side of the grid

    RETURNS:
        An integer that is the sum of Manhattan distances for all tiles.
    """
    fState = np.reshape(fromState, (-1, gridSize))
    tState = np.reshape(toState, (-1, gridSize))
    fStateDict = {}
    tStateDict = {}
    distance = 0

    for i in range(fState.shape[0]):
        for j in range(fState.shape[1]):
            if fState[i][j] != 0:
                fStateDict[fState[i][j]] = (i, j)
            
            if tState[i][j] != 0:
                tStateDict[tState[i][j]] = (i, j)
            
    for key in fStateDict.keys():
        distance += abs(fStateDict[key][0] - tStateDict[key][0]) + abs(fStateDict[key][1] - tStateDict[key][1])

    return distance

def printSucc(state):
    """
    Prints the list of all the valid successors in the puzzle.

    INPUT: 
        A state as a list.
    """
    succStates = getSucc(state)

    for succState in succStates:
        print(succState, "h={}".format(getManhattanDistance(succState)))

def getSucc(state, gridSize):
    """
    A function that gets all valid successors in the puzzle.

    INPUT: 
        A state as a list
        The size of one side of the grid

    RETURNS:
        A list of all the valid successors in the puzzle. 
    """
    succStates = []
    state = np.reshape(state, (-1, gridSize))
    ogState = np.copy(state)

    for i in range(state.shape[0]):
        for j in range(state.shape[1]):
            if state[i][j] != 0:
                continue
            
            if i - 1 >= 0:
                state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
                if (list(state.flatten()) not in succStates) and (not(np.array_equal(state, ogState))):
                    succStates.append(list(state.flatten()))
                state[i][j], state[i-1][j] = state[i-1][j], state[i][j]
            if i + 1 < state.shape[0]:
                state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
                if (list(state.flatten()) not in succStates) and (not(np.array_equal(state, ogState))):
                    succStates.append(list(state.flatten()))
                state[i][j], state[i+1][j] = state[i+1][j], state[i][j]
            if j - 1 >= 0:
                state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
                if (list(state.flatten()) not in succStates) and (not(np.array_equal(state, ogState))):
                    succStates.append(list(state.flatten()))
                state[i][j], state[i][j-1] = state[i][j-1], state[i][j]
            if j + 1 < state.shape[1]:
                state[i][j], state[i][j+1] = state[i][j+1], state[i][j]
                if (list(state.flatten()) not in succStates) and (not(np.array_equal(state, ogState))):
                    succStates.append(list(state.flatten()))
                state[i][j], state[i][j+1] = state[i][j+1], state[i][j]

    return sorted(succStates)

# TODO Implement Tree Pruning LEC 22 Games II
def solve(state, goalState, gridSize):
    """
    Implements the A* algorithm and solves the puzzle and prints a path from state to goal state along with h values, number of moves, and max queue number.

    INPUT: 
        Two states
        The size of one side of the grid
    """
    print("\nSolving...")
    startTime = time.time()
    printEvery = 5
    printGap = 5
    open = []
    closed = []
    closedStates = []
    output = []
    moves = 0
    maxQLen = 0
    h = getManhattanDistance(state, goalState, gridSize)
    heapq.heappush(open,(moves + h, state, (moves, h, -1)))

    while open:
        if maxQLen < len(open):
            maxQLen = len(open)

        n = heapq.heappop(open)
        moves = n[2][0] + 1
        closed.append(n)
        closedStates.append(n[1])

        if n[1] == goalState:
            while True:
                output.append((n[1], n[2][1], n[2][0]))
                if n[2][2] == -1:
                    break
                n = closed[n[2][2]]

            for line in reversed(output):
                print(f"Move Number: {line[2]} | Total Manhattan Distance: {line[1]}\n{np.reshape(line[0], (gridSize, gridSize))}")
                lastMoveNum = line[2]
            totalTime = time.time() - startTime
            print(f"Solve Time: {datetime.timedelta(seconds = totalTime)} | Total Moves: {lastMoveNum} | Max Queue Length: {maxQLen}")
            return
        
        succs = getSucc(n[1], gridSize)
        for succ in succs:
            if succ not in closedStates:
                h = getManhattanDistance(succ, goalState, gridSize)
                heapq.heappush(open,(moves + h, succ, (moves, h, len(closed) - 1)))

        currTime = time.time() - startTime
        if currTime > printEvery:
            print(f"Time Elapsed: {str(datetime.timedelta(seconds = currTime))[:-7]} | Current Best Cost: {open[0][0]} | Current Queue Length: {len(open)}")
            printEvery += printGap
    
def isSolvable(puzzle, gridSize, numTiles, solvedPuzzle, stats = False):
    """
    Function that returns true if given puzzle is solvable.

    INPUT: 
        An initial state
        The size of one side of the grid
        The number of tiles in the puzzle
        The solution to the puzzle
        If stats should be printed (default is false) 

    RETURN:
        True if the given puzzle is solvable.
    """
    if (numTiles == gridSize**2):
        return puzzle == solvedPuzzle

    if (numTiles <= gridSize**2-2):
        return True

    # Count inversions in given puzzle
    inv_count = 0
    empty_value_row = gridSize # default to first row as first element will not be checked 
    empty_value = 0

    for i in range(0, gridSize**2):
        for j in range(i + 1, gridSize**2):
            if (puzzle[j] != empty_value) and (puzzle[i] != empty_value) and (puzzle[i] > puzzle[j]):
                inv_count += 1

            if (puzzle[j] == 0):
                empty_value_row = gridSize - math.floor(j / gridSize)
    if stats:
        print(f"Inversions: {inv_count}")
        if gridSize % 2 == 0:
            print(f"Row of Empty Value: {empty_value_row}")

    # Logic that returns if game is solvable 
    if gridSize % 2 == 0: # Grid Size is Even
        if empty_value_row % 2 == 0: # The blank is on an even row (bottom = 1 -> top = gridSize)
            # Return true if inversion count is odd
            return (inv_count % 2 == 1)
        else: # The blank is on an odd row (bottom = 1 -> top = gridSize)
            # Return true if inversion count is even
            return (inv_count % 2 == 0)
    # Grid Size is Odd
    else:
        # Return true if inversion count is odd
        return (inv_count % 2 == 0)

def getNumberTiles(puzzle):
    """
    A function that returns the number of non-zero tiles in the puzzle.

    INPUT: 
        The puzzle  

    RETURN:
        An integer of the number of non-zero tiles in the puzzle.
    """
    numTiles = 0
    for tile in puzzle:
        if tile > 0:
            numTiles += 1

    return numTiles

def getSolvedPuzzle(gridSize, numTiles):
    """
    A function that returns what the solved puzzle should look like.

    INPUT: 
        The size of one side of the grid
        The number of tiles in the puzzle  

    RETURN:
        A list representing what the solved puzzle is.
    """
    solvedPuzzle = list(range(1, numTiles + 1))
    for _ in range(gridSize**2 - numTiles):
        solvedPuzzle.append(0)

    return solvedPuzzle

def printPuzzle(puzzle, gridSize):
    """
    A function that prints the puzzle to the console.

    INPUT: 
        The puzzle to print
        The size of one side of the grid  
    """
    print(np.reshape(puzzle, (gridSize, gridSize)))

if __name__ == "__main__":
    """
    Driver code for the program.

    FLAGS: 
        -m: *Manual Mode* Puts game in manual mode for puzzle entry
        -u: *Unsolvable Mode* Allows game to generate or accept an unsolvable game
    """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--manual", help="Puts game in manual mode for puzzle entry", action="store_true")
    parser.add_argument("-u", "--unsolvable", help="Allows game to generate or accept an unsolvable game", action="store_true")
    args = parser.parse_args()
    
    # Set booleans base on user flags
    manualEntry = args.manual
    reqSolvablePuzzle = not args.unsolvable

    waitingValidGridSize = True
    # Prompt to get valid grid size
    while waitingValidGridSize:
        userInput = input("What is the size of one side of the grid?\n")
        try:
            gridSize = int(userInput)
            if gridSize > 0:
                waitingValidGridSize = False
            else:
                print("Error: The grid size must be a positive, non-zero integer!")
        except ValueError:
            print("Error: The grid size must be an integer!")

    # Manual Mode
    if manualEntry:
        waitingValidPuzzle = True
        # Prompt to get valid puzzle
        while waitingValidPuzzle:
            print("Enter the tiles for the puzzle:")
            puzzle = []
            # Loop to fill in all the tiles
            for i in range(gridSize**2):
                waitingValidTile = True
                # Prompt to get valid tile
                while waitingValidTile:
                    userInput = input(f"Tile {i+1}: ")
                    try:
                        tileValue = int(userInput)

                        # Duplicate tile case
                        if tileValue in puzzle and tileValue != 0:
                            print(f"Error: The tile value of {tileValue} is already in the puzzle")
                            print(f"Current Puzzle: {puzzle}")
                        # Success case
                        elif tileValue >= 0 and tileValue <= gridSize**2:
                            puzzle.append(tileValue)
                            waitingValidTile = False
                        # Out of bounds case
                        else:
                            print(f"Error: Tile values must be between 0 (empty space) and {gridSize**2}!")
                            print(f"Current Puzzle: {puzzle}")
                    # Non-integer case
                    except ValueError:
                        print("Error: All tile values must be an integer!")

            # Count the number of tiles in puzzle, generate the solved puzzle, and check if the puzzle is solvable
            numTiles = getNumberTiles(puzzle)
            solvedPuzzle = getSolvedPuzzle(gridSize, numTiles)
            puzzleIsSolvable = isSolvable(puzzle, gridSize, numTiles, solvedPuzzle)

            # Blank puzzle case
            if max(puzzle) == 0:
                print("Error: Puzzle cannot only contain empty spaces!")
                print(f"Invalid Puzzle:")
                printPuzzle(puzzle, gridSize)
            # Non-sequential tiles case
            elif max(puzzle) != numTiles:
                print("Error: Puzzles must contain sequential numbered tiles only!")
                print(f"Invalid Puzzle:")
                printPuzzle(puzzle, gridSize)
            # Solvable puzzle check
            elif reqSolvablePuzzle and (not puzzleIsSolvable):
                print("Error: The given puzzle is not solvable!")
                print(f"Invalid Puzzle:")
                printPuzzle(puzzle, gridSize)
            # Valid puzzle case
            else:
                waitingValidPuzzle = False
    # Random Puzzle Mode
    else:
        waitingValidNumTiles = True
        # Prompt to get number of tiles
        while waitingValidNumTiles:
            userInput = input("How many tiles should be in the puzzle?\n")
            try:
                numTiles = int(userInput)
                if numTiles > 0 and numTiles <= gridSize**2:
                    waitingValidNumTiles = False
                else:
                    print(f"Error: The number of tiles must be between 1 and {gridSize**2}!")
            except ValueError:
                print("Error: The number of tiles must be an integer!")

        # Generate the puzzle, generate the solved puzzle, shuffle the normal puzzle, and check if the puzzle is solvable
        puzzle = getSolvedPuzzle(gridSize, numTiles)
        solvedPuzzle = getSolvedPuzzle(gridSize, numTiles)
        random.shuffle(puzzle)
        puzzleIsSolvable = isSolvable(puzzle, gridSize, numTiles, solvedPuzzle)

        # Solvable puzzle check
        if reqSolvablePuzzle:
            # Shuffle the puzzle until it is solvable
            while not puzzleIsSolvable:
                random.shuffle(puzzle)
                puzzleIsSolvable = isSolvable(puzzle, gridSize, numTiles, solvedPuzzle)

    # Print puzzle to be solved out
    print("\nPuzzle:")
    printPuzzle(puzzle, gridSize)
    
    # If the puzzle is solvable, solve it, otherwise print message
    if (puzzleIsSolvable):
        solve(puzzle, solvedPuzzle, gridSize)
    else:
        print("\nNot Solvable")
