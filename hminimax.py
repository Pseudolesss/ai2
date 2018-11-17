
from pacman_module.game import Agent
import numpy as np


class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.distances = dict()
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
        
        ret = self.initHminimax(state)
        
        return ret

    def initHminimax(self, state):

        self.nbFood = state.getNumFood()

        sons = state.generatePacmanSuccessors()

        sentinel = -np.inf
        for son in sons:
            val = self.hminimax(son[0], False, 3, 0)
            if val > sentinel:
                sentinel = val
                ret = son[1]

        return ret

    def hminimax(self, state, PacmanTurn, depth, contributions):
        
        if depth == 0 or state.isWin() or state.isLose():
            contributions = self.PHeuristic(state)
            return state.getScore() + contributions

        if PacmanTurn:
            maxGameSum = -np.inf
            sons = state.generatePacmanSuccessors()

            for son in sons:
                #contribution = self.PHeuristic(son[0], parentFood)
                contribution = 0
                gameSum = self.hminimax(son[0], not PacmanTurn, depth - 1,
                                        contribution)
                maxGameSum = max((maxGameSum, gameSum))

            return maxGameSum

        else:
            minGameSum = np.inf
            sons = state.generateGhostSuccessors(1)

            for son in sons:
                contribution = 0
                gameSum = self.hminimax(son[0], not PacmanTurn, depth - 1,
                                        contribution)
                minGameSum = min((minGameSum, gameSum))

            return minGameSum


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

        dist = self.getMinDist(state)
        foodEaten = 0

        if self.nbFood != state.getNumFood():
            foodEaten = 100 * (self.nbFood - state.getNumFood())

        return - dist + foodEaten 

    def posFood(self, foods):

        foods_pos = []
        for i in range(foods.width):
            for j in range(foods.height):
                if foods[i][j]:
                    foods_pos.append((i, j))

        return foods_pos

    def getAdj(self, state):

        
        walls = state.getWalls()

        adj = list()
        walls_height = walls.height
        walls_width = walls.width
        nb_elem = walls_height * walls_width
        lsId = lambda i, j : i * walls_height + j
        

        buff = [np.inf] * nb_elem
        for i in range(nb_elem):
            adj.append(buff.copy())

        for i in range(walls_width):
            for j in range(walls_height):
                if not walls[i][j]:
                    
                    if not walls[i - 1][j]: # left neighbour
                        adj[lsId(i ,j)][lsId(i - 1, j)] = 1

                    if not walls[i + 1][j]: # right neighbour
                        adj[lsId(i ,j)][lsId(i + 1, j)] = 1

                    if not walls[i][j - 1]: # up neighbour
                        adj[lsId(i ,j)][lsId(i , j - 1)] = 1

                    if not walls[i][j + 1]: # down neighbour
                        adj[lsId(i ,j)][lsId(i, j + 1)] = 1
                    
        return adj

    def floydWarshall(self, state, graph): 
        
        # Number of vertices in the graph 
        V = len(graph)

        lsId = lambda i, j : i * state.getWalls().height + j

        """ dist[][] will be the output matrix that will finally 
            have the shortest distances between every pair of vertices """
        """ initializing the solution matrix same as input graph matrix 
        OR we can say that the initial values of shortest distances 
        are based on shortest paths considering no 
        intermediate vertices """
        dist = list( map(lambda i : list( map(lambda j : j , i) ) , graph) )
        
        """ Add all vertices one by one to the set of intermediate 
        vertices. 
        ---> Before start of an iteration, we have shortest distances 
        between all pairs of vertices such that the shortest 
        distances consider only the vertices in the set 
        {0, 1, 2, .. k-1} as intermediate vertices. 
        ----> After the end of a iteration, vertex no. k is 
        added to the set of intermediate vertices and the 
        set becomes {0, 1, 2, .. k} 
        """
        for k in range(V): 

            # pick all vertices as source one by one 
            for i in range(V): 

                # Pick all vertices as destination for the 
                # above picked source 
                for j in range(V): 

                    # If vertex k is on the shortest path from 
                    # i to j, then update the value of dist[i][j] 
                    dist[i][j] = min(dist[i][j] , dist[i][k]+ dist[k][j]) 

        return dist

    def getMinDist(self, state):

        walls = state.getWalls()

        lsId = lambda i, j : i * walls.height + j

        dist = self.distances.get(walls, False)

        if not dist:
            dist = self.distances[walls] = self.floydWarshall(state, self.getAdj(state))
        

        ret = list()
        pacmanPos = state.getPacmanPosition()
        foods = self.posFood(state.getFood())

        for food in foods:
            ret.append(dist[lsId(pacmanPos[0], pacmanPos[1])] [lsId(food[0], food[1])])
        
        if len(ret) == 0:
            return 0
        else:
            return min(ret)
