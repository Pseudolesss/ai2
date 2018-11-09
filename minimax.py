
from pacman_module.game import Agent
import math


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

        sentinel = -math.inf

        for son in sons:
            val = self.minimax(son[0], False, {key})
            if val > sentinel:
                sentinel = val
                ret = son[1]
        
        return ret

    def minimax(self, state, PacmanTurn, visited):

        if state.isWin() or state.isLose():
            return state.getScore()

        key = self.generateKey(state, PacmanTurn)

        if PacmanTurn:
            maxGameSum = -math.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)

                if key_son in visited:  # If son state already visited
                    continue
                
                new_visited = visited.copy()
                new_visited.add(key)
                gameSum = self.minimax(son[0], not PacmanTurn, new_visited)
                maxGameSum = max((maxGameSum, gameSum))
            return maxGameSum

        else:
            minGameSum = math.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)
                if key_son in visited:  # If son state already visited
                    continue
                
                new_visited = visited.copy()
                new_visited.add(key)
                gameSum = self.minimax(son[0], not PacmanTurn, new_visited)
                minGameSum = min((minGameSum, gameSum))
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