import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mline
import numpy as np
import math

# Helper functions 
get_y = lambda coords: [loc[0] for loc in coords]
get_x = lambda coords: [loc[1] for loc in coords]

# Agents [(y,x), (y,x), (y,x)]
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
r = 8

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

### Code for vision with blocking by obstacle ###

class Box:

    def __init__(self, location) -> None:
        self.x = location[1]
        self.y = location[0]
        self.segments = self.bounds
    
    @property
    def bounds(self):
        out = [[(self.y + 0.5, self.x + 0.5), (self.y + 0.5, self.x - 0.5)],
               [(self.y + 0.5, self.x + 0.5), (self.y - 0.5, self.x + 0.5)],
               [(self.y - 0.5, self.x - 0.5), (self.y - 0.5, self.x + 0.5)],
               [(self.y - 0.5, self.x - 0.5), (self.y + 0.5, self.x - 0.5)]]
        return out

class Ray:

    def __init__(self, start: tuple, end: tuple) -> None:
        self.start_x = start[1] # x00
        self.start_y = start[0] # y00
        self.end_x = end[1]     # x10
        self.end_y = end[0]     # y10

    def check_view(self, obstacles: list[tuple[int]]) -> bool:
        
        self.reso = 50

        self.slope = math.atan2(self.end_y - self.start_y, self.end_x - self.start_x)
        
        for obstacle in obstacles:
            if self.end_x == obstacle[1] and self.end_y == obstacle[0]:
                return False
        
        for x in np.linspace(self.start_x, self.end_x, self.reso, endpoint=True):
            
            # Evaluate all points on the ray, and detect if any point intersect with an obstacle.
            # If this is the case false is retured and the therfore the end point cannot be accessed.
            if self.slope != math.pi / 2 and self.slope != - math.pi / 2:
                y = math.tan(self.slope) * (x - self.start_x) + self.start_y 

                for obstacle in obstacles:
                    if obstacle[1] - 0.5 < x < obstacle[1] + 0.5 and obstacle[0] - 0.5 < y < obstacle[0] + 0.5:
                        return False
            
            # For angles 90 and -90 the y values need to called manualy, afterwards the various y values can be 
            # used to check if an obstacle is located on any of these points, to determine if the ray is blocked
            else:

                for y in np.linspace(self.start_y, self.end_y, self.reso, endpoint=True):
            
                    for obstacle in obstacles:
                        
                        if obstacle[1] - 0.5 < x < obstacle[1] + 0.5 and obstacle[0] - 0.5 < y < obstacle[0] + 0.5:
                            return False

        return True
    
    def check_view_v2(self, obstacles: list[object]) -> bool:

        y00, x00 = self.start_y, self.start_x
        y01, x01 = self.end_y - self.start_y, self.end_x - self.start_x
        
        for obstacle in obstacles:

            for segment in obstacle.segments:

                y10, x10 = segment[0][0], segment[0][1]
                y11, x11 = segment[1][0] - segment[0][0], segment[1][1] - segment[0][1]
                
                # d = x11 y01 - x01 y11 : if 0 two lines are parralel  
                d = x11 * y01 - x01 * y11
                if d == 0:
                    continue

                s = (1/d) * ((x00 - x10) * y01 - (y00 - y10) * x01)
                t = - (1/d) * (-(x00 - x10) * y11 + (y00 - y10) * x11)

                if 0 <= s <= 1 and 0 <= t <= 1:
                    return False
        
        return True
                
# Obstacles within the map
obstacles = [(1,1), (-1,2), (-2,2), (-2,1), (-1,-1), (1,-3), (2,-3), (2,1)]
obstacles = [Box(obstacle) for obstacle in obstacles]

# View distance
r = 20

# location of main agent in the space 
agent = (2,-1)   # (y,x)

fig, ax = plt.subplots()

for i in range(-r,r+1):
    for j in range(-r,r+1):
        if i == 0 and j == 0:
            
            plt.scatter(agent[1],agent[0],color='c')
        
        elif math.sqrt(i**2 + j**2) <= r:
            # Evaulate ray from origin to end point
            # Goal is to determine if the end point can be seen/ evaluated

            line = Ray(agent, (j+agent[0], i+agent[1]))

            # Visualise points the agent can see 
            if line.check_view_v2(obstacles):
                # Point can be seen
                ax.scatter(i+agent[1], j+agent[0],color='b')
            else:
                # Point cannot be seen
                ax.scatter(i+agent[1], j+agent[0],color='r')

# Visualise objects
for obstacle in obstacles:

    rect = plt.Rectangle((obstacle.x-0.5, obstacle.y-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='none')
    ax.add_patch(rect)
# plt.scatter(agent[1],agent[0],color='c')

fig.gca().invert_yaxis()
ax.set_aspect('equal', adjustable='box')
legend_elements = [mline.Line2D([0], [0], marker='o', color='w', label='Agent',markerfacecolor='c', markersize=7),
                   mline.Line2D([0], [0], marker='o', color='w', label='Observable',markerfacecolor='b', markersize=7),
                   mline.Line2D([0], [0], marker='o', color='w', label='Not observable',markerfacecolor='r', markersize=7)]
ax.legend(handles=legend_elements)
plt.show()