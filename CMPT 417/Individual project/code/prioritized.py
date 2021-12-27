import time as timer
from single_agent_planner import compute_heuristics, a_star, get_sum_of_cost


class PrioritizedPlanningSolver(object):
    """A planner that plans for each robot sequentially."""

    def __init__(self, my_map, starts, goals):
        """my_map   - list of lists specifying obstacle positions
        starts      - [(x1, y1), (x2, y2), ...] list of start locations
        goals       - [(x1, y1), (x2, y2), ...] list of goal locations
        """

        self.my_map = my_map
        self.starts = starts
        self.goals = goals
        self.num_of_agents = len(goals)

        self.CPU_time = 0

        # compute heuristics for the low-letimeel search
        self.heuristics = []
        for goal in self.goals:
            self.heuristics.append(compute_heuristics(my_map, goal))

    def find_solution(self):
        """ Finds paths for all agents from their start locations to their goal locations."""

        max_time = len(self.my_map[0])*len(self.my_map)
        
        start_time = timer.time()
        result = []
        constraints = []
        # constraints = [{'agent':1, 'loc':[(1,3),(1,4)], 'timestep':3},{'agent':1, 'loc':[(1,3),(1,2)], 'timestep':3}]

        # constraints = [ {'agent':0, 'loc':[(1,5)], 'timestep':4},
        #                 {'agent':1, 'loc':[(1,2),(1,3)], 'timestep':1}
        # ]

        # constraints = [{'agent':0, 'loc':(1,5), 'timestep':10}]

        # Task 1.5: Designing Constraints
        # These constraints work when implementing constraint table using a list
        # constraints = [ {'agent': 1,'loc': [(1,3),(1,4)],'timestep': 2},
        #                 {'agent': 1,'loc': [(1,3)],'timestep': 2},
        #                 {'agent': 1,'loc': [(1,3),(1,2)],'timestep': 2}
        # ]

        for i in range(self.num_of_agents):  # Find path for each agent
            path = a_star(self.my_map, self.starts[i], self.goals[i], self.heuristics[i],
                          i, constraints)
            if path is None:
                raise BaseException('No solutions')
            result.append(path)
            # print("Path:",len(path))

            ##############################
            # Task 2: Add constraints here
            #         Useful timeariables:
            #            * path contains the solution path of the current (i'th) agent, e.g., [(1,1),(1,2),(1,3)]
            #            * self.num_of_agents has the number of total agents
            #            * constraints: array of constraints to consider for future A* searches

            for agent in range(self.num_of_agents):
                current_time = 0
                if agent == i:
                    continue
                for time in range(len(path)): # path is current solution for agent i
                    constraints.append({'agent': agent,'loc': [path[time]],'timestep': time, 'positive': False}) #adding vertex constraints
                    if time != 0:    
                        constraints.append({'agent': agent,'loc': [path[time],path[time-1]],'timestep': time, 'positive': False}) #adding edge constraints
                        # print("adding constraint {}".format(constraints[-1]))
                
                current_time = len(path)
                while current_time <= max_time:
                    constraints.append({'agent': agent,'loc': [path[-1]],'timestep': current_time, 'positive': False})
                    current_time += 1
            ##############################

            # print("Length: {}".format(len(self.my_map)))
            # print(self.my_map)
            for constraint in constraints:
                print("Constraint: {}".format(constraint))
            print("next")
        self.CPU_time = timer.time() - start_time

        print("\n Found a solution! \n")
        print("CPU time (s):    {:.2f}".format(self.CPU_time))
        print("Sum of costs:    {}".format(get_sum_of_cost(result)))
        print(result)
        # print(len(result)) prints out number of agents
        return result