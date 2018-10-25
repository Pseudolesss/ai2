
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
                val = self.minimax(son[0], True, 0, list(), list())
                if val > sentinel:
                    sentinel = val
                    ret = son[1]

            self.computed.update({key: ret})
            return ret  # Value associated to key (position, food)

    def minimax(self, state, PacmanTurn, contributions,
                visited_Pacman, visited_ghost):
        if state.isWin() or state.isLose():
            return state.getScore() + contributions

        key = (state.getPacmanPosition(),
               tuple(state.getGhostPositions()), state.getFood())

        if PacmanTurn:
            maxGameSum = -math.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                key_son = (son[0].getPacmanPosition(),
                           tuple(son[0].getGhostPositions()),
                           son[0].getFood())

                if key_son in visited_Pacman:
                    continue

                contribution = - self.mindist(son[0].getPacmanPosition(),
                                              son[0].getFood())
                new_visited_Pacman = visited_Pacman.copy()
                new_visited_Pacman.append(key)
                new_visited_ghost = visited_ghost.copy()
                gameSum = self.minimax(son[0], False,
                                       contributions + contribution,
                                       new_visited_Pacman, new_visited_ghost)
                maxGameSum = max((maxGameSum, gameSum))
            return maxGameSum

        else:
            minGameSum = math.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                key_son = (son[0].getPacmanPosition(),
                           tuple(son[0].getGhostPositions()),
                           son[0].getFood())

                if key_son in visited_Pacman:
                    continue

                new_visited_Pacman = visited_Pacman.copy()
                new_visited_ghost = visited_ghost.copy()
                new_visited_ghost.append(key)
                gameSum = self.minimax(son[0], True,
                                       contributions,
                                       new_visited_Pacman, new_visited_ghost)
                minGameSum = min((minGameSum, gameSum))
            return minGameSum

    def mindist(self, pos, foods):
        """
        Given a Pacman position and a food matrix, returns the shortest
        distance to a dot.
        Arguments:
        ----------
        - `pos`: Pacman's position as a pair (x,y) : x,y >= 0
        - `food`: a matrix of booleans indicating by a True value the presence
        of a dot in the maze.

        Return:
        -------
        - A integer representing the longest distance to a dot
        """
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
