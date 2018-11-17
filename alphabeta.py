
from pacman_module.game import Agent
import numpy as np


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.computed = dict()

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

        sons = state.generatePacmanSuccessors()

        sentinel = -np.inf
        alpha = -np.inf
        beta = np.inf

        for son in sons:
            val = self.minimax(son[0], False,
                                 {self.generateKey(state, True)}, alpha, beta)
            if val > sentinel:
                sentinel = val
                ret = son[1]
        
        return ret

    def minimax(self, state, PacmanTurn, visited, alpha, beta):

        if state.isWin():
            return state.getScore()

        if state.isLose():
            return state.getScore()

        key = self.generateKey(state, PacmanTurn)
        visited.add(key)

        if PacmanTurn:
            maxGameSum = -np.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)

                if key_son in visited:  # If son state already visited
                    continue
                
                gameSum = self.minimax(son[0], not PacmanTurn, visited.copy(), alpha, beta)
                maxGameSum = max((maxGameSum, gameSum))
                
                alpha = max(alpha, gameSum)
                if beta <= alpha:
                    break

            return maxGameSum

        else:
            minGameSum = np.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)
                
                if key_son in visited:  # If son state already visited
                    continue

                gameSum = self.minimax(son[0], not PacmanTurn, visited.copy(), alpha, beta)
                minGameSum = min(minGameSum, gameSum)

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
        for i in range(foods.width):
            for j in range(foods.height):
                if foods[i][j]:
                    foods_pos.extend([i, j])

        return foods_pos