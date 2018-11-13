
from pacman_module.game import Agent
import numpy as np


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.computed = dict()
        self.args = args

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        key = (state.getPacmanPosition(), tuple(
            state.getGhostPositions()), state.getFood())  # Key for dict
        computed = self.computed.get(key, False)

        if computed:
            return computed  # Return already computed result
        else:

            ret = self.initHminimax(state, key)
            self.computed.update({key: ret})
            return ret  # Value associated to key (position, food)


    def initHminimax(self, state, key):
        sons = state.generatePacmanSuccessors()

        sentinel = -np.inf  
        alpha = -np.inf
        beta = np.inf

        for son in sons:
            val = self.hminimax(son[0], False, alpha, beta, 4, 0)
            if val > sentinel:
                sentinel = val
                ret = son[1]
        
        return ret

    def hminimax(self, state, PacmanTurn, alpha, beta, depth, contributions):
        
        if depth == 0 or state.isWin() or state.isLose():
            return state.getScore() + contributions

        if PacmanTurn:
            maxGameSum = -np.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                contribution = - self.PHeuristic(son[0])
                contribution = 0
                gameSum = self.hminimax(son[0], not PacmanTurn, alpha, beta, depth - 1,
                                       contributions + contribution)
                maxGameSum = max((maxGameSum, gameSum))

                alpha = max(alpha, gameSum)
                if beta <= alpha:
                    break

            return maxGameSum

        else:
            minGameSum = np.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                contribution = 0
                gameSum = self.hminimax(son[0],  not PacmanTurn, alpha, beta, depth - 1,
                                       contributions + contribution)
                minGameSum = min((minGameSum, gameSum))

                beta = min(beta, gameSum)
                if beta <= alpha:
                    break

            return minGameSum

    def generateKey(self, state, PacmanTurn):

            pacmanPos = state.getPacmanPosition()
            ghostPos = state.getGhostPosition(1)
            foods = state.getFood()

            ret = [PacmanTurn, pacmanPos[0], pacmanPos[1], int(ghostPos[0]), int(ghostPos[1])]

            ret.extend(self.posFood(foods))

            return tuple(ret)


    def posFood(self, foods):

        foods_pos = []
        i = 0  # abscisses values
        for rows in foods:
            j = 0  # ordinates values
            for elem in rows:
                if elem:
                    foods_pos.extend([i, j])
                j += 1
            i += 1

        return foods_pos

    def PHeuristic(self, state):
        """
        Given a Pacman position and a food matrix, returns the shortest
        distance to a dot.
        Arguments:
        ----------
        - `pos`: Pacman's position as a pair (x,y) : x,y >= 0
        - `foods`: a matrix of booleans indicating by a True value the presence
        of a dot in the maze.

        Return:
        -------
        - A integer representing the longest distance to a dot
        """

        pos = state.getPacmanPosition()
        foods = state.getFood()

        foods_pos = []
        i = 0  # abscisses values
        for rows in foods:
            j = 0  # ordinates values
            for elem in rows:
                if elem:
                    foods_pos.append((i, j))
                j += 1
            i += 1

        distances = list(map(lambda x: abs(pos[0] - x[0]) + abs(pos[1] - x[1]),
                             foods_pos))

        if len(distances) == 0:
            return 0

        return min(distances)

    def GHeuristic(self, state) : 

        contribution = list(map(lambda p, g: abs(p - g),
                                   state.getPacmanPosition(),
                                   state.getGhostPosition(1)))
        contribution = sum(contribution)

        return contribution
