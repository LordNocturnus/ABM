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
import os
import sqlite3 as sql
import hashlib
import multiprocessing
import random
import sys

from collections import abc

import run_experiments
import collisions
import map_gen
import visualize
import base_solver

from cbs import CBSSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver
from single_agent_planner import get_sum_of_cost, get_longest_path_cost

import numpy as np
import pandas as pd

import itertools

## Create initial database structure

std_df_prioritized = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])
std_df_cbs_standard = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])
std_df_cbs_disjoint = pd.DataFrame([], columns=["uid", "agents", "cost", "time", "failed"])
std_df_failed = pd.DataFrame([], columns=["uid", "solver", "scenario"])

dist_df_prioritized = pd.DataFrame([], columns=["uid", "agents", "view size", "path limit", "cost", "time", "failed"])
dist_df_cbs_standard = pd.DataFrame([], columns=["uid", "agents", "view size", "path limit", "cost", "time", "failed"])
dist_df_cbs_disjoint = pd.DataFrame([], columns=["uid", "agents", "view size", "path limit", "cost", "time", "failed"])
dist_df_failed = pd.DataFrame([], columns=["uid", "solver", "view size", "path limit", "scenario"])

## Generate results 

solvers = ["prioritized", 
           "cbs-standard", 
           "cbs-disjoint", 
           "distributed prioritized", 
           "distributed cbs-standard", 
           "distributed cbs-disjoint"
           ]
maps = ["assignment_1", "assignment_2", "assignment_3"]
agents = list(range(2, 15))
view_size = list(range(2, 10))
path_limit = list(range(2, 10))
view_path_tuples = []
for v in range(2, 11):
    for p in range(2, 11):
        view_path_tuples.append((v, p))


path1 = f"maps/{maps[0]}.map"
map_1 = map_gen.MapGenerator(path1)

path2 = f"maps/{maps[1]}.map"
map_2 = map_gen.MapGenerator(path2)

path3 = f"maps/{maps[2]}.map"
map_3 = map_gen.MapGenerator(path3)

map_generators = [map_1, map_2, map_3]

score_function = get_longest_path_cost
timeout = 10 * 60

cost_value = multiprocessing.Value("i", 9999)
time_value = multiprocessing.Value("d", 9999.0)
collision_value = multiprocessing.Value("b", 1)


def fail_output(my_map: np.ndarray, starts: list[tuple[int, int]], goals: list[tuple[int, int]]) -> str:
    out = ""

    out += str(np.shape(my_map)).replace("(", "").replace(")", "\n").replace(",", "")

    my_map_str = my_map.astype(str)
    my_map_str[my_map_str == "1"] = "@"
    my_map_str = my_map_str.tolist()

    for line in my_map_str:
        out += " ".join(line)
        out += " "
        out += "\n"
    
    out += f"{len(starts)}\n"

    for start, goal in zip(starts, goals):
        out += " ".join(map(str, start))
        out += " "
        out += " ".join(map(str, goal))
        out += "\n"
    
    return out


def run_solver(my_map: np.ndarray,
               starts: list[tuple[int, int]],
               goals: list[tuple[int, int]],
               local_solver: type[base_solver.BaseSolver],
               cost: multiprocessing.Value,
               time: multiprocessing.Value,
               collision: multiprocessing.Value,
               score_func: abc.Callable[[list[list[tuple[int, int]]]], int] = get_sum_of_cost,
               **kwargs) -> None:
    try:
        solver_instance = local_solver(my_map, starts, goals, printing=False, **kwargs)
        paths = solver_instance.find_solution([])

        cost.value = score_func(paths)
        time.value = solver_instance.CPU_time

        # Check paths
        collision.value = bool(collisions.detect_collisions(paths))
    except:
        cost.value = 0
        time.value = 0
        collision.value = 0


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


if __name__ == "__main__":
    i = 0

    while True:

        for map_name, map_generator in zip(maps, map_generators):
            # Map_path
            map_name: str
            # Map generator instance
            map_generator: map_gen.MapGenerator

            num_agents = int(np.random.choice(agents, size=1, replace=False)[0])

            print(f"{i:0{5}} | solving for => {map_name=}, {num_agents=}")

            # Initial conditions
            my_map, starts, goals = map_generator.generate(num_agents)

            # uid
            uid = map_name + f"{starts}" + f"{goals}"
            uid = hashlib.sha256(uid.encode()).hexdigest()

            ## Run for each solver

            # Prioritized
            process = multiprocessing.Process(target=run_solver,
                                              args=[my_map,
                                                    starts,
                                                    goals,
                                                    PrioritizedPlanningSolver,
                                                    cost_value,
                                                    time_value,
                                                    collision_value],
                                              kwargs={"score_func": score_function})
            process.start()
            process.join(timeout=timeout)
            if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                # add to specific general data storage
                std_df_prioritized = pd.concat([std_df_prioritized,
                                                pd.DataFrame([[uid,
                                                               num_agents,
                                                               cost_value.value,
                                                               time_value.value,
                                                               collision_value.value]],
                                                             columns=["uid", "agents", "cost", "time", "failed"])],
                                               ignore_index=True)
                std_df_prioritized.to_csv("results_prioritized.csv", index=False, encoding="UTF-8")
            else:
                # Add to failure cases
                std_df_failed = pd.concat([std_df_failed,
                                           pd.DataFrame([[uid, "prioritized", fail_output(my_map, starts, goals)]],
                                                        columns=["uid", "solver", "scenario"])],
                                          ignore_index=True)
                std_df_failed.to_csv("results_failed.csv", index=False, encoding="UTF-8")

            # cbs standard
            process = multiprocessing.Process(target=run_solver,
                                              args=[my_map,
                                                    starts,
                                                    goals,
                                                    CBSSolver,
                                                    cost_value,
                                                    time_value,
                                                    collision_value],
                                              kwargs={"score_func": score_function,
                                                      "disjoint": False})
            process.start()
            process.join(timeout=timeout)
            if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                # add to specific general data storage
                std_df_cbs_standard = pd.concat([std_df_cbs_standard,
                                                pd.DataFrame([[uid,
                                                               num_agents,
                                                               cost_value.value,
                                                               time_value.value,
                                                               collision_value.value]],
                                                             columns=["uid", "agents", "cost", "time", "failed"])],
                                                ignore_index=True)
                std_df_cbs_standard.to_csv("results_cbs_standard.csv", index=False, encoding="UTF-8")
            else:
                # Add to failure cases
                std_df_failed = pd.concat([std_df_failed,
                                           pd.DataFrame([[uid, "cbs_standard", fail_output(my_map, starts, goals)]],
                                                        columns=["uid", "solver", "scenario"])],
                                          ignore_index=True)
                std_df_failed.to_csv("results_failed.csv", index=False, encoding="UTF-8")

            # cbs disjoint
            process = multiprocessing.Process(target=run_solver,
                                              args=[my_map,
                                                    starts,
                                                    goals,
                                                    CBSSolver,
                                                    cost_value,
                                                    time_value,
                                                    collision_value],
                                              kwargs={"score_func": score_function,
                                                      "disjoint": True})
            process.start()
            process.join(timeout=timeout)
            if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                # add to specific general data storage
                std_df_cbs_disjoint = pd.concat([std_df_cbs_disjoint,
                                                 pd.DataFrame([[uid,
                                                                num_agents,
                                                                cost_value.value,
                                                                time_value.value,
                                                                collision_value.value]],
                                                              columns=["uid", "agents", "cost", "time", "failed"])],
                                                ignore_index=True)
                std_df_cbs_disjoint.to_csv("results_cbs_disjoint.csv", index=False, encoding="UTF-8")
            else:
                # Add to failure cases
                std_df_failed = pd.concat([std_df_failed,
                                           pd.DataFrame([[uid, "cbs_disjoint", fail_output(my_map, starts, goals)]],
                                                        columns=["uid", "solver", "scenario"])],
                                          ignore_index=True)
                std_df_failed.to_csv("results_failed.csv", index=False, encoding="UTF-8")

            ## for distributed systems
            for view_size, path_limit in random.sample(view_path_tuples, 9):

                # Prioritized
                process = multiprocessing.Process(target=run_solver,
                                                  args=[my_map,
                                                        starts,
                                                        goals,
                                                        DistributedPlanningSolver,
                                                        cost_value,
                                                        time_value,
                                                        collision_value],
                                                  kwargs={"score_func": score_function,
                                                          "solver": PrioritizedPlanningSolver,
                                                          "view_size": view_size,
                                                          "path_limit": path_limit})
                process.start()
                process.join(timeout=timeout)
                if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                    process.close()
                    # add to specific general data storage
                    dist_df_prioritized = pd.concat([dist_df_prioritized,
                                                    pd.DataFrame([[uid,
                                                                   num_agents,
                                                                   view_size,
                                                                   path_limit,
                                                                   cost_value.value,
                                                                   time_value.value,
                                                                   collision_value.value]],
                                                                 columns=["uid",
                                                                          "agents",
                                                                          "view size",
                                                                          "path limit",
                                                                          "cost",
                                                                          "time",
                                                                          "failed"])],
                                                    ignore_index=True)
                    dist_df_prioritized.to_csv("results_dist_prioritized.csv", index=False, encoding="UTF-8")
                else:
                    process.terminate()
                    # Add to failure cases
                    dist_df_failed = pd.concat([dist_df_failed,
                                               pd.DataFrame([[uid,
                                                              "dist_prioritized",
                                                              view_size,
                                                              path_limit,
                                                              fail_output(my_map, starts, goals)]],
                                                            columns=["uid",
                                                                     "solver",
                                                                     "view size",
                                                                     "path limit",
                                                                     "scenario"])],
                                               ignore_index=True)
                    dist_df_failed.to_csv("results_dist_failed.csv", index=False, encoding="UTF-8")

                # cbs standard
                process = multiprocessing.Process(target=run_solver,
                                                  args=[my_map,
                                                        starts,
                                                        goals,
                                                        DistributedPlanningSolver,
                                                        cost_value,
                                                        time_value,
                                                        collision_value],
                                                  kwargs={"score_func": score_function,
                                                          "solver": CBSSolver,
                                                          "view_size": view_size,
                                                          "path_limit": path_limit,
                                                          "disjoint": False})
                process.start()
                process.join(timeout=timeout)
                if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                    process.close()
                    # add to specific general data storage
                    dist_df_cbs_standard = pd.concat([dist_df_cbs_standard,
                                                     pd.DataFrame([[uid,
                                                                    num_agents,
                                                                    view_size,
                                                                    path_limit,
                                                                    cost_value.value,
                                                                    time_value.value,
                                                                    collision_value.value]],
                                                                  columns=["uid",
                                                                           "agents",
                                                                           "view size",
                                                                           "path limit",
                                                                           "cost",
                                                                           "time",
                                                                           "failed"])],
                                                    ignore_index=True)
                    dist_df_cbs_standard.to_csv("results_dist_cbs_standard.csv", index=False, encoding="UTF-8")
                else:
                    process.terminate()
                    # Add to failure cases
                    dist_df_failed = pd.concat([dist_df_failed,
                                                pd.DataFrame([[uid,
                                                               "dist_cbs_standard",
                                                               view_size,
                                                               path_limit,
                                                               fail_output(my_map, starts, goals)]],
                                                             columns=["uid",
                                                                      "solver",
                                                                      "view size",
                                                                      "path limit",
                                                                      "scenario"])],
                                               ignore_index=True)
                    dist_df_failed.to_csv("results_dist_failed.csv", index=False, encoding="UTF-8")

                # cbs disjoint
                process = multiprocessing.Process(target=run_solver,
                                                  args=[my_map,
                                                        starts,
                                                        goals,
                                                        DistributedPlanningSolver,
                                                        cost_value,
                                                        time_value,
                                                        collision_value],
                                                  kwargs={"score_func": score_function,
                                                          "solver": CBSSolver,
                                                          "view_size": view_size,
                                                          "path_limit": path_limit,
                                                          "disjoint": True})
                process.start()
                process.join(timeout=timeout)
                if process.exitcode is not None and process.exitcode == 0 and not collision_value.value:
                    process.close()
                    # add to specific general data storage
                    dist_df_cbs_disjoint = pd.concat([dist_df_cbs_disjoint,
                                                      pd.DataFrame([[uid,
                                                                     num_agents,
                                                                     view_size,
                                                                     path_limit,
                                                                     cost_value.value,
                                                                     time_value.value,
                                                                     collision_value.value]],
                                                                   columns=["uid",
                                                                            "agents",
                                                                            "view size",
                                                                            "path limit",
                                                                            "cost",
                                                                            "time",
                                                                            "failed"])],
                                                     ignore_index=True)
                    dist_df_cbs_disjoint.to_csv("results_dist_cbs_disjoint.csv", index=False, encoding="UTF-8")
                else:
                    process.terminate()
                    # Add to failure cases
                    dist_df_failed = pd.concat([dist_df_failed,
                                                pd.DataFrame([[uid,
                                                               "dist_cbs_disjoint",
                                                               view_size,
                                                               path_limit,
                                                               fail_output(my_map, starts, goals)]],
                                                             columns=["uid",
                                                                      "solver",
                                                                      "view size",
                                                                      "path limit",
                                                                      "scenario"])],
                                               ignore_index=True)
                    dist_df_failed.to_csv("results_dist_failed.csv", index=False, encoding="UTF-8")
            i += 1

    print(std_df_prioritized.head())
    print(std_df_cbs_standard.head())
    print(std_df_cbs_disjoint.head())
    print(std_df_failed.head())