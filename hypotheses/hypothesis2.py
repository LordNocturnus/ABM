import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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


class GlobalSolver:

    def __init__(self, path: str, solver_name: str) -> None:
        self.solver = solver_name
        self.data = pd.read_csv(path)

    def agents_vs_cost(self):
        """
        Save data the box plots can be created where x are the number of agents, and y is the cost
        """
        # local = self.data.sort_values(by=["agents"])
        unique = self.data["agents"].unique()

        data = {}

        for agents in range(1,21):
            if agents in sorted(unique):
                data[agents] = self.data.loc[self.data['agents'] == agents, "cost"]
            else:
                data[agents] = [0]

        # fig, ax = plt.subplots()
        # ax.boxplot(data.values())
        # ax.set_xticklabels(data.keys())

        return data

    def get_length(self):
        return len(self.data.index)

class DistributedSolver(GlobalSolver):

    def __init__(self, path: str, solver_name: str) -> None:
        super().__init__(path, solver_name)

    def collect___(self):
        return ...


class FailedSolvers(GlobalSolver):
    
    def __init__(self, path: str, solver_name: str) -> None:
        super().__init__(path, solver_name)

    def count_failed(self):
        self.solvers = {
                "prioritized" : 0,
                "cbs_standard" : 0,
                "cbs_disjoint" : 0,
                "dist_prioritized" : 0,
                "dist_cbs_standard" : 0,
                "dist_cbs_disjoint" : 0
        }

        for solver in self.solvers.keys():
            self.solvers[solver] = (self.data.solver == solver).sum()

        return self.solvers

def create_boxplot(data):

    fig, ax = plt.subplots()
    ax.set_xlabel('Number of agents [-]')
    ax.set_ylabel('Maximum path length [-]')
    ax.boxplot(data.values())
    ax.set_xticklabels(data.keys())

def create_barchart(data):

    fig, ax = plt.subplots()
    ax.set_xlabel('Solver')
    ax.set_ylabel('Failure cases [%]')
    ax.bar(np.arange(0, 6), data.values())
    ax.set_xticks(np.arange(0, 6), data.keys())


# Global solvers
prioritized = GlobalSolver("data/data_5min/results_prioritized.csv", "prioritized")
cbs_standard = GlobalSolver("data/data_5min/results_cbs_standard.csv", "cbs standard")
cbs_disjoint = GlobalSolver("data/data_5min/results_cbs_disjoint.csv", "cbs disjoint")

# Distributed solvers
dist_prioritized = DistributedSolver("data/data_5min/results_dist_prioritized.csv", "distributed prioritized")
dist_cbs_standard = DistributedSolver("data/data_5min/results_dist_cbs_standard.csv", "distributed cbs standard")
dist_cbs_disjoint = DistributedSolver("data/data_5min/results_dist_cbs_disjoint.csv", "distributed cbs disjoint")

# Fauilure cases
failures = FailedSolvers("data/data_5min/results_failed.csv", "None")

## Agent vs cost
prioritized_cost = prioritized.agents_vs_cost()
cbs_standard_cost = cbs_standard.agents_vs_cost()
cbs_disjoint_cost = cbs_disjoint.agents_vs_cost()

dist_prioritized_cost = dist_prioritized.agents_vs_cost()
dist_cbs_standard_cost = dist_cbs_standard.agents_vs_cost()
dist_cbs_disjoint_cost = dist_cbs_disjoint.agents_vs_cost()

# Create regular boxplots
create_boxplot(prioritized_cost)
create_boxplot(cbs_standard_cost)
create_boxplot(cbs_disjoint_cost)
create_boxplot(dist_prioritized_cost)
create_boxplot(dist_cbs_standard_cost)
create_boxplot(dist_cbs_disjoint_cost)

# Compare outcome

def compare_solvers(solver_1, solver_2, method=str):
    comparison_cost = {"solver 1": 0,
                       "equal": 0,
                       "solver 2": 0}

    for i in range(1, 21):
        if method == "average":
            delta = np.average(solver_1[i]) - np.average(solver_2[i])
        elif method == "mean":
            delta = np.mean(solver_1[i]) - np.mean(solver_2[i])
        elif method == "Q1":
            delta = np.quantile(solver_1[i], 0.25, axis=0) - np.quantile(solver_2[i], 0.25, axis=0)
        elif method == "Q3":
            delta = np.quantile(solver_1[i], 0.75, axis=0) - np.quantile(solver_2[i], 0.75, axis=0)
        else:
            raise "The methode does not exist"

        if delta < 0:
            comparison_cost["solver 1"] += 1
        elif delta == 0:
            comparison_cost["equal"] += 1
        elif delta > 0:
            comparison_cost["solver 2"] += 1

    print(comparison_cost)

compare_solvers(prioritized_cost, dist_prioritized_cost, "average")
compare_solvers(prioritized_cost, dist_prioritized_cost, "mean")
compare_solvers(prioritized_cost, dist_prioritized_cost, "Q1")
compare_solvers(prioritized_cost, dist_prioritized_cost, "Q3")

# Failure cases
failure = failures.count_failed()

failure_rate = {
    "prioritized": failure["prioritized"] / (failure["prioritized"] + prioritized.get_length()),
    "cbs_standard": failure["cbs_standard"] / (failure["cbs_standard"] + cbs_standard.get_length()),
    "cbs_disjoint": failure["cbs_disjoint"] / (failure["cbs_disjoint"] + cbs_disjoint.get_length()),
    "dist_prioritized": failure["dist_prioritized"] / (failure["dist_prioritized"] + dist_prioritized.get_length()),
    "dist_cbs_standard": failure["dist_cbs_standard"] / (failure["dist_cbs_standard"] + dist_cbs_standard.get_length()),
    "dist_cbs_disjoint": failure["dist_cbs_disjoint"] / (failure["dist_cbs_disjoint"] + dist_cbs_disjoint.get_length()),
}

create_barchart(failure_rate)

# Additional present some unique cases.

plt.show()