import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
        self.data = pd.read_csv(path, sep=",", delimiter="")

        self.uid    = self.data["uid"]
        self.cost   = self.data["cost"]
        self.time   = self.data["time"]
        self.agents = self.data["agents"]


class DistributedSolver:

    def __init__(self, path: str, solver_name: str) -> None:
        self.solver = solver_name
        self.data = pd.read_csv(path, sep=",", delimiter="")

        self.uid            = self.data["uid"]
        self.cost           = self.data["cost"]
        self.time           = self.data["time"]
        self.agents         = self.data["agents"]
        self.path_limit     = self.data["path limit"]
        self.view_distance  = self.data["view size"]


