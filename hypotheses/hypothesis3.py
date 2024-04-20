import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

import os
import pathlib

os.chdir(pathlib.Path(__file__).parent.parent)

# Styling
plt.style.use('ggplot')

import dataclasses

solvers = [
    "Prioritized",
    "CBS_Standard",
    "CBS_Disjoint",
    "Distributed_Prioritized",
    "Distributed_CBS_Standard",
    "Distributed_CBS_Disjoint"
]

# Global planners
# -> uid (hash based on map and agent location)
# -> max path length
# -> CPU time
# -> number of agents
# -> solver used
# -> collision (True or false)
#
# Distributed planners
# -> uid
# -> max path length
# -> CPU time
# -> number of agents
# -> solver used
# -> collision (True or false)
# -> view distance
# -> path limit
#
# Unsuccessful
# -> uid
# -> map saved
# -> solver data
#
# Mixture of analyzing the data
#
#
#
#
#
#


class GlobalSolver:

    def __init__(self, path: str, solver_name: str) -> None:
        self.solver = solver_name
        self.data = pd.read_csv(path)

        self.uid = self.data["uid"]
        self.cost = self.data["cost"]
        self.time = self.data["time"]
        self.agents = self.data["agents"]

    def agents_vs_cputime(self):
        data = {}

        for agent, time in zip(self.agents, self.time):
            if agent not in data:
                data[agent] = []
            data[agent].append(time)
        return data


class DistributedSolver(GlobalSolver):

    def __init__(self, path: str, solver_name: str) -> None:
        super().__init__(path, solver_name)

        self.path_limit = self.data["path limit"]
        self.view_distance = self.data["view size"]

    def agents_vs_cputime(self):
        data = {}

        for agent, time in zip(self.agents, self.time):
            if agent not in data:
                data[agent] = []
            data[agent].append(time)
        return data


# Global solvers
prioritized = GlobalSolver("data/data_1min/results_prioritized.csv", "prioritized")
cbs_standard = GlobalSolver("data/data_1min/results_cbs_standard.csv", "cbs standard")
cbs_disjoint = GlobalSolver("data/data_1min/results_cbs_disjoint.csv", "cbs disjoint")

# Distributed solvers
dist_prioritized = DistributedSolver("data/data_1min/results_dist_prioritized.csv", "distributed prioritized")
dist_cbs_standard = DistributedSolver("data/data_1min/results_dist_cbs_standard.csv", "distributed cbs standard")
dist_cbs_disjoint = DistributedSolver("data/data_1min/results_dist_cbs_disjoint.csv", "distributed cbs disjoint")

def plot_boxplots_cputime(solver):
    plt.figure(figsize=(10, 6))
    data = solver.agents_vs_cputime()
    agents = list(data.keys())
    cpu_times = list(data.values())
    plt.boxplot(cpu_times, labels=agents)
    plt.xlabel('Number of Agents [-]')
    plt.ylabel('CPU Time [s]')
    plt.xticks(rotation=45)
    plt.show()


# plot
solvers = [prioritized, cbs_standard, cbs_disjoint, dist_prioritized, dist_cbs_standard, dist_cbs_disjoint]
for solver in solvers:
    plot_boxplots_cputime(solver)

