
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

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move corresponding
        to the state minimax sub-tree returning the highest value.

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

        for son in sons:
            val = self.minimax(son[0], False,
                               {self.generateKey(state, True)})
            if val > sentinel:
                sentinel = val
                ret = son[1]

        return ret

    def minimax(self, state, PacmanTurn, visited):
        """
        Given a pacman game state, a player turn boolean and
        a set of visited nodes, returns the value returned by 
        the corresponding minimax tree.

        Arguments:
        ----------
        - `state`: the current game state. 
        - 'PacmanTurn': If True, Pacman is playing. Otherwise
        the Ghost is playing.
        -'visited': set of context treated in the active branch of
        the tree to avoid cycles. 

        Return:
        -------
        - The number value return by the search of the tree.
        """

        if state.isWin() or state.isLose():
            return state.getScore()  # Game over, return the result

        key = self.generateKey(state, PacmanTurn)
        visited.add(key)  # the context is being visited

        if PacmanTurn:
            maxGameSum = -np.inf

            sons = state.generatePacmanSuccessors()
            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)

                if key_son in visited:  # If son context already visited
                    continue

                gameSum = self.minimax(son[0], not PacmanTurn, visited.copy())
                maxGameSum = max(maxGameSum, gameSum)

             # Ignore the node if it has no sons and it is not final
            if maxGameSum == -np.inf:
                return np.inf

            return maxGameSum

        else:
            minGameSum = np.inf

            sons = state.generateGhostSuccessors(1)
            for son in sons:
                key_son = self.generateKey(son[0], not PacmanTurn)

                if key_son in visited:  # If son context already visited
                    continue

                gameSum = self.minimax(son[0], not PacmanTurn, visited.copy())
                minGameSum = min(minGameSum, gameSum)

            # Ignore the node if it has no sons and it is not final
            if minGameSum == np.inf:
                return -np.inf

            return minGameSum

    def generateKey(self, state, PacmanTurn):
        """
        Given a game state and a player turn boolean, return a low computation
        cost key for the given context.

        Arguments:
        ----------
        - `state`: the current game state. 
        - 'PacmanTurn': If True, Pacman is playing. Otherwise the Ghost 
        is playing.

        Return:
        -------
        - List of int value. (x1, y1, x2, y2, ...)
        """

        pacmanPos = state.getPacmanPosition()
        ghostPos = state.getGhostPosition(1)
        foods = state.getFood()

        ret = [PacmanTurn, pacmanPos[0], pacmanPos[
            1], int(ghostPos[0]), int(ghostPos[1])]

        ret.extend(self.posFood(foods))

        return tuple(ret)

    def posFood(self, foods):
        """
        Given a food matrix, return the list of all dot positions according to
        the matrix.

        Arguments:
        ----------
        - `food`: A food matrix object.

        Return:
        -------
        - List of int value. (x1, y1, x2, y2, ...)
        """
        foods_pos = []
        for i in range(foods.width):
            for j in range(foods.height):
                if foods[i][j]:
                    foods_pos.extend([i, j])

        return foods_pos
