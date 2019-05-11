
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
        #print('actions(state=', state, ')\n')
        acciones = [] # 'West','North','East','South','Load','Drop'

        # Determine which actions are valid
        x = state[0][0]
        y = state[0][1]
        maxX = self.CONFIG['map_size'][0] - 1
        maxY = self.CONFIG['map_size'][1] - 1

        buildings = self.POSITIONS['building']

        if(x > 0 and (x-1, y) not in buildings): # | x
            acciones.append('West') # <=
        if(y > 0 and (x, y-1) not in buildings):
            acciones.append('North')
        if(x < maxX and (x+1, y) not in buildings): # x |
            acciones.append('East') # =>
        if(y < maxY and (x, y+1) not in buildings):
            acciones.append('South')
        if(state[1] < self.MAXBAGS and (x,y) in self.SHOPS):
            acciones.append('Load')

        ## Check if the current space is a customer
        if (state[1] > 0 and (x,y) in [(c[0], c[1]) for c in self.CUSTOMERS]):
            acciones.append('Drop')

        return acciones


    def result(self, state, action):
        '''Returns the state reached from this state when the given action is executed
        '''
        # Implement State Changes
        x = state[0][0]
        y = state[0][1]

        # Check Bounds of Map
        next_pos = (x, y)
        next_load = state[1]
        next_customers = state[2]
        if(action == 'East'):
            next_pos = (x+1, y)
        elif(action == 'South'):
            next_pos = (x, y+1)
        elif(action == 'West'):
            next_pos = (x-1, y)
        elif(action == 'North'):
            next_pos = (x, y-1)
        elif(action == 'Load'):
            next_load += 1
        elif(action == 'Drop'):
            next_load -= 1
            # Update the number of pizzas needed at the customer
            next_customers = []
            for c in state[2]:
                # If the customer is in the same square as the delivery driver
                if(c[0] == x and c[1] == y):
                    # If all pizzas have been delivered, remove customer from list
                    if(c[2] > 1):
                        # Decrease Pizzas remaining for current customer
                        next_customers.append((c[0], c[1], c[2]-1))
                else:
                    # Customer did not change
                    next_customers.append((c[0], c[1], c[2]))
            # Convert back to Tuple
            next_customers = tuple(next_customers)

        #print('result(state=', state, ', action=', action, ') => ', (next_pos, next_load, next_customers), '\n')
        return (next_pos, next_load, next_customers)


    def is_goal(self, state):
        '''Returns true if state is the final state
        '''
        #print('is_goal(state=', state, ')\n')

        # See how many deliveries are necessary
        if state == self.GOAL: return True

        return False

    def cost(self, state, action, state2):
        '''Returns the cost of applying `action` from `state` to `state2`.
           The returned value is a number (integer or floating point).
           By default this function returns `1`.
        '''
        #print('cost(state=', state, ', action=', action, ', state2=', state2, ')\n')

        if action in self.MOVES:
            # Cost is based on movement
            return self.getAttribute(state[0], "cost")

        # Otherwise Action is loading or dropping 1 pizza
        return 1

    def heuristic(self, state):
        '''Returns the heuristic for `state`
        '''
        print('heuristic4(state=', state, ')\n')
        xDistance = abs(state[0][0] - self.GOAL[0][0])
        yDistance = abs(state[0][1] - self.GOAL[0][1])
        heuristic = xDistance + yDistance
        return heuristic


    def setup (self):
        '''This method must create the initial state, final state (if desired) and specify the algorithm to be used.
           This values are later stored as globals that are used when calling the search algorithm.
           final state is optional because it is only used inside the is_goal() method

           It also must set the values of the object attributes that the methods need, as for example, self.SHOPS or self.MAXBAGS
        '''

        print('\nMAP: ', self.MAP, '\n')
        print('POSITIONS: ', self.POSITIONS, '\n')
        print('CONFIG: ', self.CONFIG, '\n')

        algorithm= simpleai.search.astar
        #algorithm= simpleai.search.greedy
        #algorithm= simpleai.search.breadth_first
        #algorithm= simpleai.search.depth_first
        #algorithm= simpleai.search.limited_depth_first

        self.MAXBAGS = self.CONFIG['maxBags']
        self.SHOPS = self.POSITIONS['pizza']
        print('SHOPS: ', self.SHOPS, '\n')

        # Initialize Customers
        # NOTE: Each customer is a tuple represented as
        #      (x, y, numPizzasOrdered)
        self.CUSTOMERS = ()
        if 'customer0' in self.POSITIONS.keys():
            self.CUSTOMERS += tuple([c + (0,) for c in self.POSITIONS['customer0']])
        if 'customer1' in self.POSITIONS.keys():
            self.CUSTOMERS += tuple([c + (1,) for c in self.POSITIONS['customer1']])
        if 'customer2' in self.POSITIONS.keys():
            self.CUSTOMERS += tuple([c + (2,) for c in self.POSITIONS['customer2']])
        if 'customer3' in self.POSITIONS.keys():
            self.CUSTOMERS += tuple([c + (3,) for c in self.POSITIONS['customer3']])
        print('CUSTOMERS: ', self.CUSTOMERS, '\n')

        initial_state = (self.AGENT_START, 0, self.CUSTOMERS) # Note: will break if immutable is included
        final_state= (self.AGENT_START, 0, ())

        return initial_state,final_state,algorithm

    def printState (self, state):
        '''Return a string to pretty-print the state '''
        pps='pos=' + str(state[0]) + ' , numPizzas=' + str(state[1]) + ' , numCustomers=' + str(state[2])
        return (pps)

    def getPendingRequests (self,state):
        ''' Return the number of pending requests in the given position (0-N).
            MUST return None if the position is not a customer.
            This information is used to show the proper customer image.
        '''
        #print('getPendingRequests(state=', state, ')\n')

        for oc in self.CUSTOMERS:
            # Check if current space is a customer
            if((oc[0],oc[1]) == state[0]):
                # Check if any pizzas are remaining
                for c in state[2]:
                    # If customer is in the space list, pizzas are remaining
                    if((oc[0],oc[1]) == (c[0],c[1])):
                        return c[2]
                # If it is not in the list, none are remaining
                return 0

        return -1 #None TODO: Python2.7

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
