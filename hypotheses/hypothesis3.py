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
            elif agent <= 17:
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
            elif agent <= 17:
                data[agent].append(time)
        return data


# Global solvers
prioritized = GlobalSolver("data/data_1min/results_prioritized.csv", "prioritized")
cbs_standard = GlobalSolver("data/data_1min/results_cbs_standard.csv", "cbs_standard")
cbs_disjoint = GlobalSolver("data/data_1min/results_cbs_disjoint.csv", "cbs_disjoint")

# Distributed solvers
dist_prioritized = DistributedSolver("data/data_1min/results_dist_prioritized.csv", "distributed_prioritized")
dist_cbs_standard = DistributedSolver("data/data_1min/results_dist_cbs_standard.csv", "distributed_cbs_standard")
dist_cbs_disjoint = DistributedSolver("data/data_1min/results_dist_cbs_disjoint.csv", "distributed_cbs_disjoint")


def plot_boxplots_cputime(solver):
    plt.figure()
    data = solver.agents_vs_cputime()
    sorted_data = sorted(data.items())
    agents = [agent for agent, _ in sorted_data]
    cpu_times = [cpu_time for _, cpu_time in sorted_data]
    plt.boxplot(cpu_times[:16], labels=agents[:16])
    plt.xlabel('Number of Agents [-]')
    plt.ylabel('CPU Time [s]')
    plt.show()
    plt.savefig(f'figures/{solver.solver}_3.svg', bbox_inches='tight')


# plot
solvers = [prioritized, cbs_standard, cbs_disjoint, dist_prioritized, dist_cbs_standard, dist_cbs_disjoint]
for solver in solvers:
    plot_boxplots_cputime(solver)


# stat test
def statistical_test_unpaired_3(solver1, solver2):
    data1 = solver1.agents_vs_cputime()
    data2 = solver2.agents_vs_cputime()

    cpu_time_1 = [cpu_time for cpu_times in data1.values() for cpu_time in cpu_times]
    cpu_time_2 = [cpu_time for cpu_times in data2.values() for cpu_time in cpu_times]

    t_statistic, p_value = stats.mannwhitneyu(cpu_time_1, cpu_time_2, alternative='less')

    print('T-statistic:', t_statistic)
    print('P-value:', p_value)

    return t_statistic, p_value


statistical_test_unpaired_3(prioritized, dist_prioritized)
statistical_test_unpaired_3(cbs_disjoint, dist_cbs_disjoint)
statistical_test_unpaired_3(cbs_standard, dist_cbs_standard)