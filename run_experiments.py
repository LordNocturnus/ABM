"""
Main file to run experiments and show animation.

Note: To make the animation work in Spyder you should set graphics backend to 'Automatic' (Preferences > Graphics > Graphics Backend).
"""

#!/usr/bin/python
import argparse
import glob
import os
from pathlib import Path
from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver  # Placeholder for Distributed Planning
from visualize import Animation
from collisions import detect_collisions
from single_agent_planner import get_sum_of_cost

import map_gen

SOLVER = "Independent"


def print_mapf_instance(my_map: list[list[bool]],
                        starts: list[tuple[int, int]],
                        goals: list[tuple[int, int]]) -> None:
    """
    Prints start location and goal location of all agents, using @ for an obstacle, . for a open cell, and 
    a number for the start location of each agent.
    
    Example:
        @ @ @ @ @ @ @ 
        @ 0 1 . . . @ 
        @ @ @ . @ @ @ 
        @ @ @ @ @ @ @ 
    """
    print('Start locations')
    print_locations(my_map, starts)
    print('Goal locations')
    print_locations(my_map, goals)


def print_locations(my_map: list[list[bool]],
                    locations: list[tuple[int, int]]) -> None:
    """
    See docstring print_mapf_instance function above.
    """
    starts_map = [[-1 for _ in range(len(my_map[0]))] for _ in range(len(my_map))]
    for i in range(len(locations)):
        starts_map[locations[i][0]][locations[i][1]] = i
    to_print = ''
    for x in range(len(my_map)):
        for y in range(len(my_map[0])):
            if starts_map[x][y] >= 0:
                to_print += str(starts_map[x][y]) + ' '
            elif my_map[x][y]:
                to_print += '@ '
            else:
                to_print += '. '
        to_print += '\n'
    print(to_print)


def import_mapf_instance(filename: str) -> tuple[list[list[bool]], list[tuple[int, int]], list[tuple[int, int]]]:
    """
    Imports mapf instance from instances folder. Expects input as a .txt file in the following format:
        Line1: #rows #columns (number of rows and columns)
        Line2-X: Grid of @ and . symbols with format #rows * #columns. The @ indicates an obstacle, whereas . indicates free cell.
        Line X: #agents (number of agents)
        Line X+1: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent 1)
        Line X+2: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent 2)
        Line X+n: xCoordStart yCoordStart xCoordGoal yCoordGoal (xy coordinate start and goal for Agent n)
        
    Example:
        4 7             # grid with 4 rows and 7 columns
        @ @ @ @ @ @ @   # example row with obstacle in every column
        @ . . . . . @   # example row with 5 free cells in the middle
        @ @ @ . @ @ @
        @ @ @ @ @ @ @
        2               # 2 agents in this experiment
        1 1 1 5         # agent 1 starts at (1,1) and has (1,5) as goal
        1 2 1 4         # agent 2 starts at (1,2) and has (1,4) as goal
    """
    if not Path(filename).is_file():
        raise BaseException(filename + " does not exist.")
    with open(filename, 'r') as f:
        # first line: #rows #columns
        line = f.readline()
        rows, columns = [int(x) for x in line.split(' ')]
        rows = int(rows)
        # #rows lines with the map
        my_map: list[list[bool]] = []
        for r in range(rows):
            line = f.readline()
            my_map.append([])
            for cell in line:
                if cell == '@':
                    my_map[-1].append(True)
                elif cell == '.':
                    my_map[-1].append(False)
        # #agents
        line = f.readline()
        num_agents = int(line)
        # #agents lines with the start/goal positions
        starts = []
        goals = []
        for a in range(num_agents):
            line = f.readline()
            sx, sy, gx, gy = [int(x) for x in line.split(' ')]
            starts.append((sx, sy))
            goals.append((gx, gy))
    return my_map, starts, goals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runs various MAPF algorithms')
    parser.add_argument('--instance', type=str, default=None,
                        help='The name of the instance file(s)')
    parser.add_argument('--batch', action='store_true', default=False,
                        help='Use batch output instead of animation')
    parser.add_argument('--solver', type=str, default=SOLVER,
                        help='The solver to use (one of: {CBS, CBSDisjoint,Independent,Prioritized}), defaults to ' + str(SOLVER))

    args = parser.parse_args()
    # Hint: Command line options can be added in Spyder by pressing CTRL + F6 > Command line options. 
    # In PyCharm, they can be added as parameters in the configuration.
    if args.instance is None:
        p = input("Please indicate which instance to run:")
        if "maps/" in p:
            args.instance = os.path.join(os.getcwd(), p)
        else:
            args.instance = os.path.join(os.getcwd(), "instances", p)

    result_file = open("results.csv", "w", buffering=1)

    for file in sorted(glob.glob(args.instance)):

        print(f"***Import instance {file}***")

        if "maps/" in file:
            my_map, starts, goals = map_gen.MapGenerator(file).generate(20)
        else:
            my_map, starts, goals = import_mapf_instance(file)

        print_mapf_instance(my_map, starts, goals)

        if args.solver == "CBS":
            print("***Run CBS***")
            cbs = CBSSolver(my_map, starts, goals, disjoint=False)
            paths = cbs.find_solution([])
        elif args.solver == "CBSDisjoint":
            print("***Run CBS***")
            cbs = CBSSolver(my_map, starts, goals)
            paths = cbs.find_solution([])
        elif args.solver == "Independent":
            print("***Run Independent***")
            indep = IndependentSolver(my_map, starts, goals)
            paths = indep.find_solution([])
        elif args.solver == "Prioritized":
            print("***Run Prioritized***")
            prio = PrioritizedPlanningSolver(my_map, starts, goals)
            paths = prio.find_solution([])
        elif args.solver == "DistributedPrioritized":  # Wrapper of distributed planning solver class
            print("***Run Distributed Planning***")
            distri = DistributedPlanningSolver(my_map, starts, goals, solver=PrioritizedPlanningSolver, view_size=3, path_limit=3)
            paths = distri.find_solution([])
        elif args.solver == "DistributedCBS":  # Wrapper of distributed planning solver class
            print("***Run Distributed Planning***")
            distri = DistributedPlanningSolver(my_map, starts, goals, solver=CBSSolver, disjoint=False, view_size=3, path_limit=3)
            paths = distri.find_solution([])
        elif args.solver == "DistributedCBSDisjoint":  # Wrapper of distributed planning solver class
            print("***Run Distributed Planning***")
            distri = DistributedPlanningSolver(my_map, starts, goals, solver=CBSSolver, view_size=3, path_limit=3)
            paths = distri.find_solution([])
        else: 
            raise RuntimeError("Unknown solver!")

        temp = detect_collisions(paths)
        if not len(temp.keys()) == 0:
            print(temp)
            #raise ValueError
        cost = get_sum_of_cost(paths)
        result_file.write("{},{}\n".format(file, cost))
        print("######################################################################################################")

        if not args.batch:
            print("***Test paths on a simulation***")
            animation = Animation(my_map, starts, goals, paths)
            # animation.save("output.mp4", 1.0) # install ffmpeg package to use this option
            animation.show()
    result_file.close()
