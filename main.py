#import heapq to use for the priority queue implementation
import heapq

#Import time to time how long it takes to find a solution
from time import time

class Puzzle():
    
    def __init__(self, startState, goalState, heuristic):
        #Start state attribute to store the Grid instance for the initial start state
        self.startState = Grid(startState)

        #Goal state attribute to store the Grid instance for the goal state
        self.goalState = Grid(goalState)

        #Heuristic attribute to store which heuristic is being used, either 1 for misplaced tiles, or 2 for Manhattan distances
        self.heuristic = heuristic

        #Grid ID attribute to uniquely identify each grid in the priority queue
        self.gridID = 0

        #Open set is a priority queue which stores the list of discovered grids to explore
        self.openSet = []
       
        #Initialise the puzzle by finding the f score of the start state and add it to the open set
        hValue = self.calculateHeuristuc(self.startState)
        gValue = self.calculateG(self.goalState)
        fValue = hValue + gValue
        self.addToOpenSet(self.startState, fValue)

    def calculateHeuristuc(self, grid):
        """
        Function to return the result of the specified heuristic function on a grid
        Parameters: Grid instance to apply the heuristic function to
        Returns: The value of applying the heuristic function to the input grid
        """
        
        if int(self.heuristic) == int(1):
            return self.hMisplacedValue(grid)
        else:
            return self.hManhattanValue(grid)


    def hManhattanValue(self, currentState):
        """
        Function to calculate the Manhattan heuristic value of a grid
        Parameters: The grid instance to calculate the Manhattan heuristic of
        Returns: The sum of the Manhattan distances of each tile
        """
        #Iterate over every tile in the grid, skipping over the blank tile
        hValue = 0
        for y in range(0,3):
            for x in range(0,3):
                if currentState.tiles[y][x] != 0:
                    tile = currentState.tiles[y][x]
                    goalY, goalX = self.getGoalTilePosition(tile)
                    distance = 0
                    distance += abs(y - goalY)
                    distance += abs(x - goalX)
                    hValue = hValue + distance

        return hValue


    def hMisplacedValue(self, currentState):
        """
        Function to calculate the number of misplaced tiles
        Parameters: Grid instance to apply the misplace tile heuristic to
        Returns: The number of misplaced tiles in the grid
        """
        
        hValue = 0
        for y in range(0,3):
            for x in range(0,3):
                #Check if the tile (not the empty tile) is in the correct position, if not, add 1 to the hValue
                if currentState.tiles[y][x] != 0 and currentState.tiles[y][x] != self.goalState.tiles[y][x]:
                    hValue = hValue + 1
        return hValue

    def calculateG(self, grid):
        """
        Function to retrieve and return the g value of the current grid
        Parameters: Grid instance to find the g value for
        Returns: The g value of the grid
        """
        
        return grid.gValue
    

    def getGoalTilePosition(self, tile):
        """
        Function to return position of a specified tile in the goal state
        Parameters: A tile (in the form of a number 1-8) which we want to find the position of in the goal state
        Returns: The x and y position of the tile in the goal state
        """

        #Iterate over every tile in the goal state until we find it, and return the value of x and y, i.e. the position
        for y in range(0,3):
            for x in range(0,3):
                if self.goalState.tiles[y][x] == tile:
                    return (y,x)

    def displaySolution(self, currentGrid):
        """
        Function to output the solution. It does so by printing the parent grid of each grid
        Parameters: The grid which has been found as the goal state
        Returns: None
        """

        #Iterate over every grids parent grid in turn until the parent is null, i.e. we are at the grid we started at
        solutionPath = []
        totalMoves = 0 
        while currentGrid.getParent():
            solutionPath.append(currentGrid)
            currentGrid = currentGrid.getParent()
            totalMoves += 1
        solutionPath.reverse()
        
        for grid in solutionPath:
            grid.printGrid()

        #Display how many moves there have been
        print()
        print("Solution found, number of moves: " + str(totalMoves))

    def isOpenSetEmpty(self):
        """
        Funtion to check whether the open set is empty
        Parameters: None
        Returns: None
        """
        
        return len(self.openSet) == 0

    def isSolution(self, grid):
        """
        Function to check whether the input grid is the goal state
        Parameters: Grid instance to check if its a solution
        Returns: Boolean whether grid is solution
        """
        
        for y in range(0,3):
            for x in range(0,3):
                #Check if each tile is in the correct space as in the goal state grid
                if grid.tiles[y][x] != self.goalState.tiles[y][x]:
                    return False
        return True
   
    def addToOpenSet(self, grid, fValue):
        """
        Function to add the discovered grid to the priority queue
        Parameters: The grid to add to the priority queue and its f value
        Returns: None
        """

        #Add new grid to the priority queue, along with its f value and unique ID, then increment the grid ID
        heapq.heappush(self.openSet, (fValue, self.gridID, grid))
        self.gridID += 1
        
    def popFromOpenSet(self):
        """
        Function to pop the first grid off the priority queue, this will be the grid with the lowest f score.
        Parameters: None
        Returns: The grid with the lowest f score in the priority queue
        """

        #Pop from the priority queue the grid with the lowest f score and return it
        fValue, gridID, grid = heapq.heappop(self.openSet)
        return grid

class Grid:
    
    def __init__(self, tiles, parent=None):
        self.tiles = tiles
        self.fValue = 0
        self.parent = parent
        
        #If the node has a parent, its g value is the parents g value add 1
        if self.parent:
            self.gValue = self.parent.gValue + 1
        else:
            self.gValue = 0


    def getChildGrids(self):
        """
        Function to generate all children grids (i.e. all grids that can be generated)
        from a parent grid (up, down, left and right)
        Parameters: None
        Returns: A list of all child grids of the grid
        """
        
        #List all directions a square can move (left, right, up and down)
        childGrids = []

        #Get the position of the blank tile in the grid
        blankYPosition, blankXPosition = self.locateEmptyTile()

        for move in range(0,4):

            #Take a copy of the parent grid which we update as the child
            childTiles = [row[:] for row in self.tiles]

            #Create the new child grid as an instance of the Grid class
            child = Grid(childTiles, self)

            if move == 0:
                #Make the move upwards which will generate a new child of the parent grid
                possible = child.makeMoveUp(blankYPosition, blankXPosition)
                if possible:
                    #Add the child grid to a list of all children
                    childGrids.append(child)       

            if move == 1:
                #Make the move downwards which will generate a new child of the parent grid
                possible = child.makeMoveDown(blankYPosition, blankXPosition)
                if possible:
                    #Add the child grid to a list of all children
                    childGrids.append(child)   

            if move == 2:
                #Make the move leftwards which will generate a new child of the parent grid
                possible = child.makeMoveLeft(blankYPosition, blankXPosition)
                if possible:
                    #Add the child grid to a list of all children
                    childGrids.append(child)   

            if move == 3:
                #Make the move rightwards which will generate a new child of the parent grid
                possible = child.makeMoveRight(blankYPosition, blankXPosition)
                if possible:
                    #Add the child grid to a list of all children
                    childGrids.append(child)
                    

        return childGrids

    def makeMoveUp(self, tileYPosition, tileXPosition):
        """
        Function which takes in two tiles on the grid and swaps them
        Parameters: The position of tile1 and position of tile2, the two tiles to be swapped on the board
        Returns: None
        """
        
        #Extract the X and Y points from the two tiles to be swapped
        tile1XPosition = tileYPosition
        tile1YPosition = tileXPosition
        tile2XPosition = tileYPosition + 1
        tile2YPosition = tileXPosition

        if -1 < tile2XPosition < 3:
            #Swap the two tiles
            tempTile = self.tiles[tile2XPosition][tile2YPosition]
            self.tiles[tile2XPosition][tile2YPosition] = self.tiles[tile1XPosition][tile1YPosition]
            self.tiles[tile1XPosition][tile1YPosition] = tempTile
            return True
        return False

    def makeMoveDown(self, tileYPosition, tileXPosition):
        """
        Function which takes in two tiles on the grid and swaps them
        Parameters: The position of tile1 and position of tile2, the two tiles to be swapped on the board
        Returns: None
        """
        
        #Extract the X and Y points from the two tiles to be swapped
        tile1XPosition = tileYPosition
        tile1YPosition = tileXPosition
        tile2XPosition = tileYPosition - 1
        tile2YPosition = tileXPosition

        if -1 < tile2XPosition < 3:
            #Swap the two tiles
            tempTile = self.tiles[tile2XPosition][tile2YPosition]
            self.tiles[tile2XPosition][tile2YPosition] = self.tiles[tile1XPosition][tile1YPosition]
            self.tiles[tile1XPosition][tile1YPosition] = tempTile
            return True
        return False


    def makeMoveLeft(self, tileYPosition, tileXPosition):
        """
        Function which takes in two tiles on the grid and swaps them
        Parameters: The position of tile1 and position of tile2, the two tiles to be swapped on the board
        Returns: None
        """
        
        #Extract the X and Y points from the two tiles to be swapped
        tile1XPosition = tileYPosition
        tile1YPosition = tileXPosition
        tile2XPosition = tileYPosition
        tile2YPosition = tileXPosition + 1

        if -1 < tile2YPosition < 3:
            #Swap the two tiles
            tempTile = self.tiles[tile2XPosition][tile2YPosition]
            self.tiles[tile2XPosition][tile2YPosition] = self.tiles[tile1XPosition][tile1YPosition]
            self.tiles[tile1XPosition][tile1YPosition] = tempTile
            return True
        return False

    def makeMoveRight(self, tileYPosition, tileXPosition):
        """
        Function which takes in two tiles on the grid and swaps them
        Parameters: The position of tile1 and position of tile2, the two tiles to be swapped on the board
        Returns: None
        """
        
        #Extract the X and Y points from the two tiles to be swapped
        tile1XPosition = tileYPosition
        tile1YPosition = tileXPosition
        tile2XPosition = tileYPosition
        tile2YPosition = tileXPosition - 1

        if -1 < tile2YPosition < 3:
            #Swap the two tiles
            tempTile = self.tiles[tile2XPosition][tile2YPosition]
            self.tiles[tile2XPosition][tile2YPosition] = self.tiles[tile1XPosition][tile1YPosition]
            self.tiles[tile1XPosition][tile1YPosition] = tempTile
            return True
        return False

    def locateEmptyTile(self):
        """
        Function to find the position of the empty tile in the grid
        Parameters: None
        Returns: The x and y position of the empty tile on the board
        """

        #Iterate over every tile in the 3x3 grid and check whether it is equal to 0
        for y in range(0,3):
            for x in range(0,3):
                if self.tiles[y][x] == 0:
                    return y, x

    def printGrid(self):
        """
        Function to print out the grid in a nice way to the screen
        Parameters: None
        Returns: None
        """

        #Iterate over every tile in the grid and output its value
        for y in range(0,3):
            for x in range(0,3):
                print(self.tiles[y][x], end=" ")
            print()
        print("-----")


    def getParent(self):
        """
        Function to return the parent grid of the grid
        Parameters: None
        Returns: The parent of the grid
        """
        
        return self.parent

    def __eq__(self, other):
        """
        Override the equality class to comapre a set of tiles on the grid
        """
        
        return self.tiles == other.tiles

    def __hash__(self):
        """
        Override the hash class to hash the tiles on the grid
        """
        
        return hash(str(self.tiles))

def solve(heuristic, startState, goalState):
    """
    Function to solve the 8-puzzle
    Parameters: The heuristic function to use, given as a number, 1 is misplaced tiles, 2 is Manhattan distances
    Returns: None
    """
    
    start_time = time()
    #Closed set variable to keep track of visited grids
    closedSet = set()

    #Define new Puzzle instance which contains the rules of the puzzle
    puzzle = Puzzle(startState, goalState, heuristic)
   
    solved = False
    #Continue while there are grids in the open set and there has not been found a solution
    while not puzzle.isOpenSetEmpty() and not solved:

        #Get the best grid to go to next from the open set priority queue and add it to the closed set
        currentGrid = puzzle.popFromOpenSet()
        closedSet.add(currentGrid)

        #Get all the child grids from the current grid - these are grids that can be generated from the current grid
        childrenGrids = currentGrid.getChildGrids()

        #Iterate over each child grid and calculate each of their f values using the specified heuristuc
        for childGrid in childrenGrids:
            #First, check if the child grid is the solution, i.e. the goal states
            if not puzzle.isSolution(childGrid):
                hValue = puzzle.calculateHeuristuc(childGrid)
                gValue = puzzle.calculateG(childGrid)
                fValue = hValue + gValue

                #If the child grid is not in the closed set, i.e. it is new, add it to the open set
                if childGrid not in closedSet:
                    puzzle.addToOpenSet(childGrid, fValue)

            else:
                solved = True
                end_time = time()
                puzzle.displaySolution(childGrid)
                print("Time taken to find solution: " + str(end_time - start_time))
                return

    print("No solution found...")
    return

def inputGrid():
    """
    Function to get the user to input a grid
    Parameters: None
    Returns: A 2D array representing the grid the user has entered
    """
    
    row1=[]
    row2=[]
    row3=[]
    grid = []

    #Get the user to enter the grid in three steps, entering each row, separated by spaces
    while(len(row1)!=3):
        row1 = input("Row 1: ")
        row1=([int(s) for s in row1.split(" ")])

    while(len(row2)!=3):
        row2 = input("Row 2: ")
        row2=([int(s) for s in row2.split(" ")])

    while(len(row3)!=3):
        row3 = input("Row 3: ")
        row3=([int(s) for s in row3.split(" ")])
    
    #Add rows to the 2D array
    grid.append(row1)
    grid.append(row2)
    grid.append(row3)
    
    return grid

if __name__ == "__main__":
    #Request the heuristic to be used from the user (must be either 1 or 2)
    print("Welcome to the 8-Puzzle solver")
    print("This program will solve the 8-puzzle using the A* algorithm")
    print("You can select betwwen two different admissible heuristic functions")
    print("These are 1: Number of misplaced tiles, and 2: sum of Manhattan distances")
    print()
    print("When entering a grid, please ensure you enter 1-8, with 0 representing the blank square, leave a space between each number")
    print()
    print("Enter start state: ")
    startState = inputGrid()

    print("Enter goal state: ")
    goalState = inputGrid()

    #Get the heuristic function option from the user
    heuristic = -1
    while heuristic!=1 and heuristic!=2:
        heuristic = int(input("Please select a heuristc, 1 or 2: "))

    print("Solving puzzle...")
    solve(heuristic, startState, goalState)
     
