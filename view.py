import matplotlib.pyplot as plt
import numpy as np
import math

# Helper functions 
get_y = lambda coords: [loc[0] for loc in coords]
get_x = lambda coords: [loc[1] for loc in coords]

# Agents
agent1 = [(0,0), (0,1), (0,2), (1,2), (2,2)]
agent2 = [(1,1), (1,2), (1,3), (2,3), (2,2)]
agent3 = [(5,1), (5,2), (5,3), (6,3), (6,4)]
agent4 = [(7,1), (7,2), (7,3), (7,4), (7,5)]

# All agents for evaluation 
agents = [agent1, agent2, agent3, agent4]
colors = ['r','c','b','g']

# Obstacles
obstacles = [(5,0), (6,0), (7,0), (6,1), (6,2)]

# View distance
r = 2

def detect_in_range(timestep: int, paths: list[list[tuple]], range: int) -> list[list]:
    
    locations = [path[timestep] for path in paths]
    agent_views = []
    
    for m_id, m_agent in enumerate(locations):
        
        agent_view = []
        
        for s_id, s_agent in enumerate(locations):
            
            # Go to next if the main and secondary agent are the same
            if m_id == s_id:
                view = False
            else:
                # Detect if agent is within range
                dist = math.sqrt((m_agent[0] - s_agent[0])**2 + (m_agent[1]-s_agent[1])**2)
                if dist <= range:
                    view = True
                else:
                    view = False
            
            agent_view.append(view) 
        
        agent_views.append(agent_view)

    return agent_views


res = detect_in_range(0, agents, r)

fig, ax = plt.subplots()

### VISUALISATION ###
# Visualise paths
for id, agent in enumerate(agents):

    ax.plot(get_x(agent), get_y(agent), label=f"Agent #{id}")
    
    for loc in agent:
        circle = plt.Circle((loc[1], loc[0]), r, color=colors[id], alpha=0.2, fill=False)
        ax.add_patch(circle)

# Visualise objects
for obstacle in obstacles:

    rect = plt.Rectangle((obstacle[1]-0.5, obstacle[0]-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='k')
    ax.add_patch(rect)

fig.gca().invert_yaxis()
ax.set_aspect('equal', adjustable='box')
plt.legend()
plt.show()