from matplotlib import pyplot as plt
import pandas as pd
import scipy as sp
import numpy as np
import os
import pathlib

plt.style.use("ggplot")

if __name__ == "__main__":
    cwd = pathlib.Path(os.getcwd())
    prio = pd.read_csv(cwd.parent.joinpath("results_prioritized.csv"),
                       encoding="UTF-8", encoding_errors='ignore')
    dist_prio = pd.read_csv(cwd.parent.joinpath("results_dist_prioritized.csv"),
                            encoding="UTF-8", encoding_errors='ignore')
    print(sp.stats.mannwhitneyu(prio["cost"][prio["uid"].isin(dist_prio["uid"])],
                                dist_prio["cost"][dist_prio["uid"].isin(prio["uid"])],
                                alternative="greater"))

    cbs_standard = pd.read_csv(cwd.parent.joinpath("results_cbs_standard.csv"),
                               encoding="UTF-8", encoding_errors='ignore')
    dist_cbs_standard = pd.read_csv(cwd.parent.joinpath("results_dist_cbs_standard.csv"),
                                    encoding="UTF-8", encoding_errors='ignore')
    print(sp.stats.mannwhitneyu(
        cbs_standard["cost"][cbs_standard["uid"].isin(dist_cbs_standard["uid"])],
        dist_cbs_standard["cost"][dist_cbs_standard["uid"].isin(cbs_standard["uid"])],
        alternative="greater"))

    cbs_dist = pd.read_csv(cwd.parent.joinpath("results_cbs_disjoint.csv"),
                           encoding="UTF-8", encoding_errors='ignore')
    dist_cbs_dist = pd.read_csv(cwd.parent.joinpath("results_dist_cbs_disjoint.csv"),
                                encoding="UTF-8", encoding_errors='ignore')
    print(sp.stats.mannwhitneyu(
        cbs_dist["cost"][cbs_dist["uid"].isin(dist_cbs_dist["uid"])],
        dist_cbs_dist["cost"][dist_cbs_dist["uid"].isin(cbs_dist["uid"])],
        alternative="greater"))

