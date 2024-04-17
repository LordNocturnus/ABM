# ------------------------------------------------------------------------------------------------------------------------
#                                       Generate data set for further analysis
# ------------------------------------------------------------------------------------------------------------------------
# General idea;
#   -> inputs
#       - map:      assignment_1, assignment_2, assignment_3 (3)
#       - #agent:   There are theoretical maxima [138-1, 130-1, 126-1] (open spots - walls -1) however it is rather 
#                   uncertain that these may be solved within a realistic amount of time. Therefore the value can be
#                   anywhere from 0/1 to the maxima. (~128, ~256)  
#       - seed:     random identifier ...   => effecting starting locations
#       - method:  prioritized, cbs (standard and disjoint), distributed (standard, disjoint and prioritized) (6)
#       - Global or distributed: 0 (global) or 1 (distributed)
#       - Feed_forward: 
#       - View_distance:
#
#   -> output
#       - CPU time
#       - total path length
#
#   -> idea
#       - Encode as much information as possible of the scenario into a single binary or hexadecimal number 
#       - only store the final cost and time values as actual integer/ floating point numbers within the .db
#
#   -> style
#       - sha 256 hash to store the map, various agent start, finish locations
#
#   -> workflow
#       - generate a scenario configuration, this scenario configuration will be run for all 6 solvers
#       - Afterwards the output is stored for each and a new scenario is generated
# ________________________________________________________________________________________________________________________

import sqlite3 as sql
import hashlib

import run_experiments
import collisions
import map_gen
import visualize

from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver

from single_agent_planner_v2 import get_sum_of_cost

import numpy as np
import pandas as pd


## Create initial database structure

std_df_prioritized = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])
std_df_cbs_standard = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])
std_df_cbs_disjoint = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])

## Generate results 

solvers = ["prioritized", 
           "cbs-standard", 
           "cbs-disjoint", 
           "distributed prioritized", 
           "distributed cbs-standard", 
           "distributed cbs-disjoint"
           ]
maps = ["assignment_1", "assignment_2", "assignment_3"]
agents = list(range(1,5))
vr = list(range(2,10))
ff = list(range(2,10))


path1 = f"maps/{maps[0]}.map"
map_1 = map_gen.MapGenerator(path1)

path2 = f"maps/{maps[1]}.map"
map_2 = map_gen.MapGenerator(path2)

path3 = f"maps/{maps[2]}.map"
map_3 = map_gen.MapGenerator(path3)

map_generators = [map_1, map_2, map_3]


def run_prioritized(my_map: np.ndarray, 
                    starts: list[tuple[int, int]], 
                    goals: list[tuple[int, int]]) -> tuple[int, float, bool]:
    
    # Solve using prioritized
    try:
        paths = PrioritizedPlanningSolver(my_map, starts, goals, printing=False, recursive=False).find_solution([])

        cost = sum([len(el) for el in paths])
        time = 1

        # Check paths
        collision = bool(collisions.detect_collisions(paths))
    except BaseException:
        cost, time, collision = 0, 0, 1

    return cost, time, collision


def run_cbs_standard(my_map: np.ndarray,
                     starts: list[tuple[int, int]], 
                     goals: list[tuple[int, int]]) -> tuple[int, float, bool]:
    
    # Solve using prioritized
    try:
        paths = CBSSolver(my_map, starts, goals, printing=False, disjoint=False).find_solution([])

        cost = sum([len(el) for el in paths])
        time = 1

        # Check paths
        collision = bool(collisions.detect_collisions(paths))
    except BaseException:
        cost, time, collision = 0, 0, 1

    return cost, time, collision


def run_cbs_disjoint(my_map: np.ndarray,
                     starts: list[tuple[int, int]], 
                     goals: list[tuple[int, int]]) -> tuple[int, float, bool]:
    
    # Solve using prioritized
    try:
        paths = CBSSolver(my_map, starts, goals, printing=False, disjoint=True).find_solution([])

        cost = sum([len(el) for el in paths])
        time = 1

        # Check paths
        collision = bool(collisions.detect_collisions(paths))
    except BaseException:
        cost, time, collision = 0, 0, 1

    return cost, time, collision


i = 0

while i < 1000:

    for map_name, map_generator in zip(maps, map_generators):
        # Map_path
        map_name: str
        # Map generator instance
        map_generator: map_gen.MapGenerator

        num_agents = int(np.random.choice(agents, size=1, replace=False)[0])
        view_range = int(np.random.choice(vr, size=1, replace=False)[0])
        path_comms = int(np.random.choice(ff, size=1, replace=False)[0])

        print(f"{i:0{5}} | solving for => {map_name=}, {num_agents=}, {view_range=}, {path_comms=}")

        # Initial conditions
        my_map, starts, goals = map_generator.generate(num_agents)

        # uid
        uid = map_name + f"{starts}" + f"{goals}"
        uid = hashlib.sha256(uid.encode()).hexdigest()

        ## Run for each solver

        # Prioritized
        cost, time, collision = run_prioritized(my_map, starts, goals)

        if not collision:
            # add to specific general data storage
            std_df_prioritized = pd.concat([std_df_prioritized, 
                                            pd.DataFrame([[uid, num_agents, cost, time, collision]],
                                                        columns=["uid", "agents", "cost", "time", "failed"])], 
                                            ignore_index=True)
        else:
            # Add to failure cases
            pass


        # cbs standard

        cost, time, collision = run_cbs_standard(my_map, starts, goals)
        
        if not collision:
            # add to specific general data storage
            std_df_cbs_standard = pd.concat([std_df_cbs_standard, 
                                            pd.DataFrame([[uid, num_agents, cost, time, collision]],
                                                        columns=["uid", "agents", "cost", "time", "failed"])], 
                                            ignore_index=True)
        else:
            # add to failure cases
            pass
        
        # cbs disjoint
        cost, time, collision = run_cbs_disjoint(my_map, starts, goals)
        
        if not collision:
            # add to specific general data storage
            std_df_cbs_disjoint = pd.concat([std_df_cbs_disjoint, 
                                            pd.DataFrame([[uid, num_agents, cost, time, collision]],
                                                        columns=["uid", "agents", "cost", "time", "failed"])], 
                                            ignore_index=True)
        else:
            # add to failure cases
            pass

        i += 1

print(std_df_prioritized.head())
print(std_df_cbs_standard.head())
print(std_df_cbs_disjoint.head())