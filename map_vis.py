import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

from run_experiments import import_mapf_instance
from map_gen import MapGenerator
from matplotlib import colors


def map_vis(map_name: str, num_agents: int = 0) -> None:
    """
        Create illustrations of the various test case maps

    :param map_name:    {str}   name of the map, the path will automatically be adapted based of if
                                instance maps are provided or assignment maps.
    
    :param num_agents:  {int}   number of agents to be spawned within the map.
    """
    if "assignment" in map_name:
        my_map, agents_start, agents_end = MapGenerator(f"maps/{map_name}.map").generate(num_agents)
    else:
        my_map, agents_start, agents_end = import_mapf_instance(f"instances/{map_name}.txt")

    my_map = np.array(my_map)

    cmap = colors.ListedColormap(['#D4D4D4', '#333333'])

    fig, ax = plt.subplots()
    ax.imshow(my_map, cmap=cmap)

    color_palette = [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf',  # Teal
        '#aec7e8',  # Light Blue
        '#ffbb78',  # Light Orange
        '#98df8a',  # Light Green
        '#ff9896',  # Light Red
        '#c5b0d5',  # Light Purple
        '#c49c94',  # Light Brown
        '#f7b6d2',  # Light Pink
        '#c7c7c7',  # Light Gray
        '#dbdb8d',  # Light Olive
        '#9edae5',  # Light Teal
        '#ff0000',  # Bright Red
        '#00ff00',  # Bright Green
        '#0000ff',  # Bright Blue
        '#ffff00',  # Bright Yellow
        '#ff00ff',  # Bright Magenta
    ]

    ## Add agents

    agent = 0

    for agent_start, agent_end in zip(agents_start, agents_end):

        start = plt.Circle(agent_start[::-1], 0.3, facecolor=color_palette[agent - 1], edgecolor="k")
        end = mpatches.Rectangle([el - 0.4 for el in agent_end[::-1]], 0.8, 0.8, linewidth=1,
                                 edgecolor=color_palette[agent - 1], facecolor='none')

        ax.add_patch(start)
        ax.add_patch(end)
        ax.annotate(agent, agent_start[::-1], color='w', weight='bold',
                    fontsize=7, ha='center', va='center')

        agent += 1

    plt.axis('off')

    plt.savefig(f'figures/{map_name}.pdf', bbox_inches='tight')

    plt.close()


for i in range(1, 51):
    print(f"=== Generating map visualization of map {i} ===")
    map_vis(f'test_{i}')

map_vis("assignment_1")
map_vis("assignment_2")
map_vis("assignment_3")

map_vis("hypotheses/hypothesis_1")
map_vis("hypotheses/hypothesis_2")