
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
        key = (state.getPacmanPosition(), tuple(
            state.getGhostPositions()), state.getFood())  # Key for dict
        computed = self.computed.get(key, False)

        if computed:
            return computed  # Return already computed result
        else:

            sons = state.generatePacmanSuccessors()

            sentinel = -math.inf

            for son in sons:
                val = self.minimax(son[0], 4, True)
                if val > sentinel:
                    sentinel = val
                    ret = son[1]

            self.computed.update({key: ret})
            return ret  # Value associated to key (position, food)

    def minimax(self, state, depth, PacmanTurn):
        if depth == 0 or state.isWin() or state.isLose():
            return state.getScore()

        if PacmanTurn:
            maxGameSum = -math.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                gameSum = self.minimax(son[0], depth-1, False)
                maxGameSum = max((maxGameSum, gameSum))
            return maxGameSum

        else:
            minGameSum = math.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                gameSum = self.minimax(son[0], depth-1, True)
                minGameSum = min((minGameSum, gameSum))
            return minGameSum
