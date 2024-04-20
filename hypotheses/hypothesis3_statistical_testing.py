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

    def collect___(self):
        return ...

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

# def statistical_test_unpaired(solvers):
#     agent_model, cpu_time_model = solvers[1].agents_vs_cputime().items()
#     agent_global, cpu_time_global = solvers[0].agents_vs_cputime().items()
#
#
#     t_statistic_3, p_value_3 = stats.ttest_ind(cpu_time_model, cpu_time_global)
#
#     # print('T-statistic hypothesis II', t_statistic_2, 'p-value hypothesis II', p_value_2)
#     print('T-statistic hypothesis III', t_statistic_3, 'p-value hypothesis III', p_value_3)

def statistical_test_unpaired(solver1, solver2):
    # Extract data for both solvers
    data1 = solver1.agents_vs_cputime()
    data2 = solver2.agents_vs_cputime()

    # Iterate over unique agent counts
    unique_agents = set(data1.keys()).union(data2.keys())
    for agent_count in unique_agents:
        cpu_times1 = data1.get(agent_count, [])
        cpu_times2 = data2.get(agent_count, [])

        # Perform unpaired t-test
        t_statistic, p_value = stats.ttest_ind(cpu_times1, cpu_times2)

        # Print the results
        print(f'Agent Count: {agent_count}')
        print('T-statistic:', t_statistic)
        print('P-value:', p_value)
        print()

# def statistical_test_paired(solver1, solver2):
#     # Extract data for both solvers
#     data1 = solver1
#     data2 = solver2
#
#     # Iterate over unique agent counts
#     unique_agents = set(data1.keys()).intersection(data2.keys())
#     for agent_count in unique_agents:
#         cpu_times1 = data1.get(agent_count, [])
#         cpu_times2 = data2.get(agent_count, [])
#
#         # Perform paired t-test
#         t_statistic, p_value = stats.ttest_rel(cpu_times1, cpu_times2)
#
#         # Print the results
#         print(f'Agent Count: {agent_count}')
#         print('T-statistic:', t_statistic)
#         print('P-value:', p_value)
#         print()


def statistical_test_paired(solvers):
    range_model = x
    cpu_time_model = y
    t_statistic_4, p_value_4 = stats.ttest_rel(range_model, cpu_time_model)

    forward_com = x
    cpu_time_model = y
    t_statistic_5, p_value_5 = stats.ttest_rel(forward_com, cpu_time_model)

    print('T-statistic hypothesis IV', t_statistic_4, 'p-value hypothesis IV', p_value_4)
    print('T-statistic hypothesis V', t_statistic_5, 'p-value hypothesis V', p_value_5)


#plot
# solvers = [prioritized, cbs_standard, cbs_disjoint, dist_prioritized, dist_cbs_standard, dist_cbs_disjoint]
# for solver in solvers:
#     plot_boxplots_cputime(solver)

#solvers
solvers_prio = [prioritized, dist_prioritized]
solvers_cbs = [cbs_standard, dist_cbs_standard]
solvers_dis = [cbs_disjoint, dist_cbs_disjoint]

#stat tests
statistical_test_unpaired(prioritized, dist_prioritized)