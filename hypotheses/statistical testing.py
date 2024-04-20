from scipy import stats
#from hypothesis2 import prioritized, cbs_standard, cbs_disjoint, dist_prioritized, dist_cbs_standard, dist_cbs_disjoint
from hypothesis3 import prioritized, cbs_standard, cbs_disjoint, dist_prioritized, dist_cbs_standard, dist_cbs_disjoint


def statistical_test_unpaired(solver1, solver2):
    # Extract data for both solvers
    data1 = solver1.agents_vs_cputime()
    data2 = solver2.agents_vs_cputime()

    # Set up test data dictionary
    statistical_test_data = {}

    # Iterate over unique agent counts
    unique_agents = set(data1.keys()).union(data2.keys())
    for agent_count in unique_agents:
        cpu_times1 = data1.get(agent_count, [])
        cpu_times2 = data2.get(agent_count, [])

        # Perform unpaired t-test
        t_statistic, p_value = stats.ttest_ind(cpu_times1, cpu_times2)

        # Add data to test data dictionary
        statistical_test_data[agent_count] = (t_statistic, p_value)

        # Print the results
        print(f'Agent Count: {agent_count}')
        print('T-statistic:', t_statistic)
        print('P-value:', p_value)
        print()

    return statistical_test_data


def statistical_test_paired(solver1, solver2):
    # Extract data for both solvers
    data1 = solver1
    data2 = solver2

    # Set up test data dictionary
    statistical_test_data = {}

    # Iterate over unique agent counts
    unique_agents = set(data1.keys()).intersection(data2.keys())
    for agent_count in unique_agents:
        cpu_times1 = data1.get(agent_count, [])
        cpu_times2 = data2.get(agent_count, [])

        # Perform paired t-test
        t_statistic, p_value = stats.ttest_rel(cpu_times1, cpu_times2)

        # Add data to test data dictionary
        statistical_test_data[agent_count] = (t_statistic, p_value)

        # Print the results
        print(f'Agent Count: {agent_count}')
        print('T-statistic:', t_statistic)
        print('P-value:', p_value)
        print()

    return statistical_test_data


#solvers
solvers_prio = [prioritized, dist_prioritized]
solvers_cbs = [cbs_standard, dist_cbs_standard]
solvers_dis = [cbs_disjoint, dist_cbs_disjoint]

#stat tests
statistical_test_unpaired(prioritized, dist_prioritized)