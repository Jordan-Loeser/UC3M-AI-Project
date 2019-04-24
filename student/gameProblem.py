
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
# from simpleai.search import breadth_first,depth_first,astar,greedy
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below

    MAP=None
    POSITIONS=None
    INITIAL_STATE=None
    GOAL=None
    CONFIG=None
    AGENT_START=None
    SHOPS=None
    CUSTOMERS=None
    MAXBAGS = 0

    MOVES = ('West','North','East','South')

   # --------------- Common functions to a SearchProblem -----------------

    def actions(self, state):
        '''Returns a LIST of the actions that may be executed in this state
        '''
        print('actions(state=', state, ')\n')
        acciones = [] # 'West','North','East','South'

        # Determine which actions are valid
        x = state[0]
        y = state[1]
        maxX = self.CONFIG['map_size'][0]
        maxY = self.CONFIG['map_size'][1]

        if(x > 0):
            acciones.append('East')
        if(y > 0):
            acciones.append('North')
        if(x < maxX):
            acciones.append('West')
        if(y < maxY):
            acciones.append('South')

        return acciones


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        print('result(state=', state, ', action=', action, ')\n')

        # Implement State Changes
        x = state[0]
        y = state[1]

        if(action == 'West'):
            next_state = (x+1, y)
        elif(action == 'South'):
            next_state = (x, y+1)
        elif(action == 'East'):
            next_state = (x-1, y)
        elif(action == 'North'):
            next_state = (x, y-1)

        return next_state


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        print('is_goal(state=', state, ')\n')
        return False

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        print('cost(state=', state, ', action=', action, ', state2=', state2, ')\n')
        return 1

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        print('heuristic(state=', state, ')\n')
        #xDiff = abs(state[0] - self.final_state[0])
        #yDiff = abs(state[1] - self.final_state[1])

        return 0


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print('\nMAP: ', self.MAP, '\n')
        print('POSITIONS: ', self.POSITIONS, '\n')
        print('CONFIG: ', self.CONFIG, '\n')

        initial_state = self.AGENT_START
        final_state= None

        algorithm= simpleai.search.astar
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        self.SHOPS = self.POSITIONS['building']
        print('SHOPS: ', self.SHOPS, '\n')

        self.CUSTOMERS = self.POSITIONS['customer1']
        print('CUSTOMERS: ', self.CUSTOMERS, '\n')

        self.MAXBAGS = 2 # Defined by problem 1

        return initial_state,final_state,algorithm

    def printState (self, state):
        '''Return a string to pretty-print the state '''
        print('printState(state=', state, ')\n')

        pps=''
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N).
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        print('getPendingRequests(state=', state, ')\n')
        return None

    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

    def getAttribute (self, position, attributeName):
        '''Returns an attribute value for a given position of the map
           position is a tuple (x,y)
           attributeName is a string

           Returns:
               None if the attribute does not exist
               Value of the attribute otherwise
        '''
        tileAttributes=self.MAP[position[0]][position[1]][2]
        if attributeName in tileAttributes.keys():
            return tileAttributes[attributeName]
        else:
            return None

    def getStateData (self,state):
        stateData={}
        pendingItems=self.getPendingRequests(state)
        if pendingItems >= 0:
            stateData['newType']='customer{}'.format(pendingItems)
        return stateData

    # THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
    def initializeProblem(self,map,positions,conf,aiBaseName):
        self.MAP=map
        self.POSITIONS=positions
        self.CONFIG=conf
        self.AGENT_START = tuple(conf['agent']['start'])

        initial_state,final_state,algorithm = self.setup()
        if initial_state == False:
            print('-- INITIALIZATION FAILED')
            return True

        self.INITIAL_STATE=initial_state
        self.GOAL=final_state
        self.ALGORITHM=algorithm
        super(GameProblem,self).__init__(self.INITIAL_STATE)

        print('-- INITIALIZATION OK')
        return True

    # END initializeProblem
