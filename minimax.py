
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
        self.visited = set()

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
        key = self.generateKey(state, True)  # Key for dict
        computed = self.computed.get(key, False)

        if computed:
            return computed  # Return already computed result
        else:

            ret = self.initMinimax(state, key)

            self.computed.update({key: ret})
            return ret  # Value associated to key (position, food)

    def initMinimax(self, state, key):
        sons = state.generatePacmanSuccessors()

        sentinel = -np.inf

        self.visited.clear()
        self.visited.add(key)

        for son in sons:
            val = self.minimax(son[0], False)
            if val > sentinel:
                sentinel = val
                ret = son[1]
        
        return ret

    def minimax(self, state, PacmanTurn):

        if state.isWin():
            key = self.generateKey(state, PacmanTurn)
            self.visited.add(key)
            return state.getScore()

        if state.isLose():
            key = self.generateKey(state, PacmanTurn)
            self.visited.add(key)
            return -np.inf

        key = self.generateKey(state, PacmanTurn)
        self.visited.add(key)

        if PacmanTurn:
            maxGameSum = -np.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)

                if key_son in self.visited:  # If son state already visited
                    continue
                
                gameSum = self.minimax(son[0], not PacmanTurn)
                maxGameSum = max(maxGameSum, gameSum)
            if maxGameSum == -np.inf:
                return np.inf
            return maxGameSum

        else:
            minGameSum = np.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)
                if key_son in self.visited:  # If son state already visited
                    continue

                gameSum = self.minimax(son[0], not PacmanTurn)
                minGameSum = min(minGameSum, gameSum)
            if minGameSum == np.inf:
                return -np.inf
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