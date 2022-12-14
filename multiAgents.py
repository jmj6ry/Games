# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util
import sys
import random

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        #minimum ghost distance
        minGhostDist = sys.maxsize
        for ghost in newGhostStates:
            dist = manhattanDistance(newPos, ghost.getPosition())
            if (dist < minGhostDist):
                minGhostDist = dist

        minFoodDist = sys.maxsize
        for food in newFood.asList():
            dist = manhattanDistance(newPos, food)
            if (dist < minFoodDist):
                minFoodDist = dist

    

        return successorGameState.getScore() + 20/(minFoodDist+1) - (2/(minGhostDist+1) * 1.5)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth, player):
            actions = gameState.getLegalActions(player)
            #check if depth is 0 or at a end state
                #return static evaluation of position
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return [self.evaluationFunction(gameState)]

            #if all players played, decrement depth and play again
            if player == gameState.getNumAgents() - 1:
                depth -= 1
                child = 0
            else:
                #next player plays
                child = player + 1

            #maximizing player
            if player == 0:
                maxEval = -sys.maxsize-1
                bestMove = None
                for action in actions:
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, child)[0]
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = action
                return maxEval, bestMove
            #minimizing player
            else:
                minEval = sys.maxsize
                bestMove = None
                for action in actions:
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, child)[0]
                    if eval < minEval:
                        minEval = eval
                        bestMove = action
                return minEval, bestMove
        
        eval, move = minimax(gameState, self.depth, self.index)
        return move
       
       
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth, alpha, beta, player):
            actions = gameState.getLegalActions(player)
            #check if depth is 0 or at a end state
                #return static evaluation of position
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return [self.evaluationFunction(gameState)]

            #if all players played, decrement depth and play again
            if player == gameState.getNumAgents() - 1:
                depth -= 1
                child = 0
            else:
                #next player plays
                child = player + 1

            #maximizing player
            if player == 0:
                maxEval = -sys.maxsize-1
                bestMove = None
                for action in actions:
                    if beta < maxEval:
                        break
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, alpha, beta, child)[0]
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = action
                    alpha = max(maxEval, alpha)
                return maxEval, bestMove
            #minimizing player
            else:
                minEval = sys.maxsize
                bestMove = None
                for action in actions:
                    if minEval < alpha:
                        break
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, alpha, beta, child)[0]
                    if eval < minEval:
                        minEval = eval
                        bestMove = action
                    beta = min(minEval, beta)
                return minEval, bestMove
        
        eval, move = minimax(gameState, self.depth, -sys.maxsize-1, sys.maxsize, self.index)
        return move

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, depth, player):
            actions = gameState.getLegalActions(player)
            #check if depth is 0 or at a end state
                #return static evaluation of position
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return [self.evaluationFunction(gameState)]

            #if all players played, decrement depth and play again
            if player == gameState.getNumAgents() - 1:
                depth -= 1
                child = 0
            else:
                #next player plays
                child = player + 1
            
            numActions = len(gameState.getLegalActions(player))

            #maximizing player
            if player == 0:
                maxEval = -sys.maxsize-1
                bestMove = None
                for action in actions:
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, child)[0]
                    if eval > maxEval:
                        maxEval = eval
                        bestMove = action
                #print("Best Action:" + str(bestMove))
                return maxEval, bestMove
            #minimizing player
            else:
                exMax = 0
                for action in actions:
                    newState = gameState.generateSuccessor(player, action)
                    eval = minimax(newState, depth, child)[0]
                    exMax+= eval
                randAction = actions[random.randrange(0, numActions)]
                return (exMax/len(actions)), randAction
        
        eval, move = minimax(gameState, self.depth, self.index)
        return move


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()

    "*** YOUR CODE HERE ***"
    
    #minimum ghost distance
    minGhostDist = sys.maxsize
    for ghost in ghostStates:
        dist = manhattanDistance(pos, ghost.getPosition())
        if (dist < minGhostDist):
            minGhostDist = dist

    minFoodDist = sys.maxsize
    for food in food.asList():
        dist = manhattanDistance(pos, food)
        if (dist < minFoodDist):
            minFoodDist = dist



    return currentGameState.getScore() + 20/(minFoodDist+1) - (2/(minGhostDist+1))

# Abbreviation
better = betterEvaluationFunction
