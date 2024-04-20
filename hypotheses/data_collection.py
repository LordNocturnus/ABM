import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import os
import pathlib

os.chdir(pathlib.Path(__file__).parent.parent)

# Styling
plt.style.use('ggplot')

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

    def viewsize_vs_cpu(self):
        """
        Save data the box plots can be created where x are the number of agents, and y is the cost
        """
        unique = self.data["view size"].unique()

        data = {}

        for agents in range(2,11):
            if agents in sorted(unique):
                data[agents] = self.data.loc[self.data['view size'] == agents, "time"]
            else:
                data[agents] = [0]

        return data
    
    def pathlimit_vs_cpu(self):
        """
        Save data the box plots can be created where x are the number of agents, and y is the cost
        """
        unique = self.data["path limit"].unique()

        data = {}

        for agents in range(2,11):
            if agents in sorted(unique):
                data[agents] = self.data.loc[self.data['path limit'] == agents, "time"]
            else:
                data[agents] = [0]

        return data
    
    # maybe effect on cost

class FailedSolvers(GlobalSolver):
    
    def __init__(self, path: str, solver_name: str) -> None:
        super().__init__(path, solver_name)

    def count_failed(self):
        self.solvers = {
                "prioritized": 0,
                "cbs_standard": 0,
                "cbs_disjoint": 0,
                "dist_prioritized": 0,
                "dist_cbs_standard": 0,
                "dist_cbs_disjoint": 0
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

def create_histogram(data):

    fig, ax = plt.subplots()
    ax.hist(data, density=True, bins=np.arange(1,21)-0.5)  # density=False would make counts
    ax.set_xlabel('Data')
    ax.set_ylabel('successful runs [%]')
    ax.set_xticks(np.arange(1,21))


# Global solvers
prioritized = GlobalSolver("data/data_v3/results_prioritized.csv", "prioritized")
cbs_standard = GlobalSolver("data/data_v3/results_cbs_standard.csv", "cbs standard")
cbs_disjoint = GlobalSolver("data/data_v3/results_cbs_disjoint.csv", "cbs disjoint")

# Distributed solvers
dist_prioritized = DistributedSolver("data/data_v3/results_dist_prioritized.csv", "distributed prioritized")
dist_cbs_standard = DistributedSolver("data/data_v3/results_dist_cbs_standard.csv", "distributed cbs standard")
dist_cbs_disjoint = DistributedSolver("data/data_v3/results_dist_cbs_disjoint.csv", "distributed cbs disjoint")

# Failure cases
glob_failures = FailedSolvers("data/data_v3/results_failed.csv", "None")
dist_failures = FailedSolvers("data/data_v3/results_dist_failed.csv", "None")

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
glob_failure = glob_failures.count_failed()
dist_failure = dist_failures.count_failed()

failure_rate = {
    "prioritized": glob_failure["prioritized"] / (glob_failure["prioritized"] + prioritized.get_length()),
    "cbs_standard": glob_failure["cbs_standard"] / (glob_failure["cbs_standard"] + cbs_standard.get_length()),
    "cbs_disjoint": glob_failure["cbs_disjoint"] / (glob_failure["cbs_disjoint"] + cbs_disjoint.get_length()),
    "dist_prioritized": dist_failure["dist_prioritized"] / (dist_failure["dist_prioritized"] + dist_prioritized.get_length()),
    "dist_cbs_standard": dist_failure["dist_cbs_standard"] / (dist_failure["dist_cbs_standard"] + dist_cbs_standard.get_length()),
    "dist_cbs_disjoint": dist_failure["dist_cbs_disjoint"] / (dist_failure["dist_cbs_disjoint"] + dist_cbs_disjoint.get_length()),
}

create_barchart(failure_rate)

# Additional present some unique cases.


## Data analysis of succesfull data to explore if
# Can be used to mention if valid points can be made on the extreme regions, or if just not enough data
# is available, to reliably comment about these points.

create_histogram(prioritized.data['agents'])
create_histogram(cbs_standard.data['agents'])
create_histogram(cbs_disjoint.data['agents'])
create_histogram(dist_prioritized.data['agents'])
create_histogram(dist_cbs_standard.data['agents'])
create_histogram(dist_cbs_disjoint.data['agents'])

# similar for the vision

# plt.show()

## Filter results to excluded higher agent count
## check if the cpu vs ... are implemented correctly
## Investigating more local, with constant factor and changing other

# dist_prioritized.pathlimit_vs_cpu()[10]
# fig, ax = plt.subplots()
# ax.hist(dist_prioritized.pathlimit_vs_cpu()[10], density=False)  # density=False would make counts

# # plt.show()

# fig, ax = plt.subplots()
# ax.hist(dist_cbs_disjoint.data["time"], density=False, bins=150)  # density=False would make counts

# plt.show()