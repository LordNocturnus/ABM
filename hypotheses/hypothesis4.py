# Hypothesis formulation for Hypothesis 4
# Test = Friedman (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.friedmanchisquare.html)
# Formulation of H0: Increasing the view range of all agents, has an effect on the CPU time.
# Test outcome, increasing the View range has no effect on the cpu time (Rejection 0 hypothesis)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

import os
import pathlib

import scipy.stats

os.chdir(pathlib.Path(__file__).parent.parent)


if __name__ == "__main__":
    # Styling
    plt.style.use('ggplot')

    data = pd.read_csv("data/data_v3/results_dist_prioritized.csv")

    # data = pd.read_csv("data/data_v3/results_dist_cbs_standard.csv")
    # data = pd.read_csv("data/data_v3/results_dist_cbs_disjoint.csv")

    friedman_data = [
        [],
        [],
        [],
        [],
    ]

    uniques = data["uid"].unique()

    for unique in uniques:
        rel = data.loc[data["uid"] == unique]
        
        if len(set(rel["view size"])) >= 4:

            ## Collect data
            u_viewsize = sorted(list(set(rel["view size"])))
            
            for i in range(4):
            # rel = rel.sort_values(by=["view size"])

                el = rel.loc[rel["view size"] == u_viewsize[i], "time"].iloc[[0]]

                friedman_data[i].append(el)

    res = scipy.stats.friedmanchisquare(*friedman_data)
    print(f"test statistic: {res.statistic}, test p-value: {res.pvalue}")