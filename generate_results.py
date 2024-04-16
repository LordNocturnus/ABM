# ------------------------------------------------------------------------------------------------------------------------
#                                       Generate data set for further analysis
# ------------------------------------------------------------------------------------------------------------------------
# General idea;
#   -> inputs
#       - map:      assignment_1, assignment_2, assignment_3 (3)
#       - #agent:   There are theoretical maxima [138-1, 130-1, 126-1] (openspots - walls -1) however it is rather 
#                   uncertain that these may be soved within a realistic amount of time. Therfore the value can be
#                   anywhere from 0/1 to the maxima. (~128, ~256)  
#       - seed:     random identifier ...   => effecting starting locations
#       - methode:  prioritized, cbs (standard and disjoint), distributed (standard, disjoint and prioritized) (6)
#       - Global or distributed: 0 (global) or 1 (distributed)
#       - Feed_forward: 
#       - View_distance:
#
#   -> output
#       - CPU time
#       - total path legnth
#
#   -> idea
#       - Encode as much information as possible of the scenario into a single binary or hexidecimal number 
#       - only store the final cost and time values as actual integer/ floating point numbers within the .db
#
#   -> style
#       - 0x _._.__.___._._._
#       - global, map, agent, seed, solver, view range, forward communication
#
#   -> pre generation
#       - Pre generated a range of valid uid which can be decoded and afterwards utelised within the solver
#       - Then randomly sample from the list, decode the uid and solve the map
#       - In this way not all cases need to evaluated, however we are sampling from the full range.
# ________________________________________________________________________________________________________________________

import sqlite3 as sql

import run_experiments
import collisions
import map_gen
import visualize

from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver

from single_agent_planner_v2 import get_sum_of_cost

## Create initial database structure
connection = sql.connect("results.db")
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS prioritized")
cursor.execute("""CREATE TABLE prioritized(
               uid TEXT,
               cost INTEGER,
               time FLOAT
               )""")

def encode(global_, map_, agents_, seed_, solver_, view_, comms_):    
    return "0x" + f"{global_:0{1}x}" + f"{map_:0{1}x}" + f"{agents_:0{2}x}" + f"{seed_:0{3}x}" + f"{solver_:0{1}x}" + f"{view_:0{1}x}" + f"{comms_:0{1}x}"



## Generate results 

solver      = "prioritized"
my_map_path      = "maps/assignment_1.map"

for i in range(1,40):
    for j in range(1,20):

        num_agents  = i
        seed        = j

        uid = encode(0, 0, num_agents, seed, 0, 0, 0)

        try:
            # Solve 
            my_map, starts, goals = map_gen.MapGenerator(my_map_path, seed=seed).generate(num_agents)
            paths = PrioritizedPlanningSolver(my_map, starts, goals, printing=False, recursive=False).find_solution([])

            # Check paths
            collision = bool(collisions.detect_collisions(paths))
            if collision:
                raise BaseException

            cost = sum([len(el) for el in paths])
            time = 0

            cursor.execute("INSERT INTO prioritized VALUES (?, ?, ?)",
                        (uid, cost, time))
        except:
            pass
    
    connection.commit()