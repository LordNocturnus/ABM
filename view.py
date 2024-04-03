import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mline
import numpy as np
import math

def generate_view_map() -> dict[list[tuple[int,int]]]:
    
    view_map = {}

    # Evaluate view for all posible locations Precomp step, to reduce computational requirements. 
    view_map["y" ,"x"] = agent_vision()
    
    return view_map

def fov(m_id: int, locations: list[tuple[int, int]], view_radius: int) -> list[bool]:
    
    visibility = []

    m_agent = locations[m_id]
        
    for s_id, s_agent in enumerate(locations):
        
        # Go to next if the main and secondary agent are the same
        if m_id == s_id:
            view = False
        else:
            # Detect if agent is within range
            dist = math.sqrt((m_agent[0] - s_agent[0])**2 + (m_agent[1]-s_agent[1])**2)
            if dist <= view_radius:
                view = True
            else:
                view = False
        
        visibility.append(view)

    return visibility


def fov_blocking(m_id: int, locations: list[tuple[int, int]], view_radius: int,
                 obstacles: list[tuple[int,int]], DEBUG: bool=False) -> list[bool]:
    
    m_agent = locations[m_id]
    obstacles = [Box(obstacle) for obstacle in obstacles]
    
    visibility = []

    view_map = agent_vision(m_agent, view_radius, obstacles, DEBUG)
        
    for s_id, s_agent in enumerate(locations):
            
        # Go to next if the main and secondary agent are the same
        if m_id == s_id:
            view = False
        else:
            if s_agent in view_map:
                view = True
            else:
                view = False

        visibility.append(view)

    return visibility


class Box:

    def __init__(self, location) -> None:
        self.x = location[1]
        self.y = location[0]
        self.segments = self.bounds
    
    @property
    def bounds(self):
        padding = 0.49
        out = [[(self.y + padding, self.x + padding), (self.y + padding, self.x - padding)],
               [(self.y + padding, self.x + padding), (self.y - padding, self.x + padding)],
               [(self.y - padding, self.x - padding), (self.y - padding, self.x + padding)],
               [(self.y - padding, self.x - padding), (self.y + padding, self.x - padding)]]
        return out


class Ray:

    def __init__(self, start: tuple, end: tuple) -> None:
        self.start_x = start[1]
        self.start_y = start[0]
        self.end_x = end[1]
        self.end_y = end[0]

    def check_view(self, obstacles: list[tuple[int]]) -> bool:
        
        self.reso = 50

        self.slope = math.atan2(self.end_y - self.start_y, self.end_x - self.start_x)
        
        for obstacle in obstacles:
            if self.end_x == obstacle.x and self.end_y == obstacle.y:
                return False
        
        for x in np.linspace(self.start_x, self.end_x, self.reso, endpoint=True):
            
            # Evaluate all points on the ray, and detect if any point intersect with an obstacle.
            # If this is the case false is retured and the therfore the end point cannot be accessed.
            if self.slope != math.pi / 2 and self.slope != - math.pi / 2:
                y = math.tan(self.slope) * (x - self.start_x) + self.start_y 

                for obstacle in obstacles:
                    if obstacle.x - 0.5 < x < obstacle.x + 0.5 and obstacle.y - 0.5 < y < obstacle.y + 0.5:
                        return False
            
            # For angles 90 and -90 the y values need to called manualy, afterwards the various y values can be 
            # used to check if an obstacle is located on any of these points, to determine if the ray is blocked
            else:

                for y in np.linspace(self.start_y, self.end_y, self.reso, endpoint=True):
            
                    for obstacle in obstacles:
                        
                        if obstacle.x - 0.5 < x < obstacle.x + 0.5 and obstacle.y - 0.5 < y < obstacle.y + 0.5:
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


def agent_vision(agent_loc: tuple[int, int], view_radius: int, obstacles: list[object], 
                 DEBUG: bool=False) -> list[tuple[int, int]]:
    """
    Returns the points the agent can be view based on the its view radius and the agents within the environment
    """

    points_in_vision = []
    
    for i in range(-view_radius, view_radius+1):
        for j in range(-view_radius, view_radius+1):
            if i == 0 and j == 0:
                
                continue
            
            elif math.sqrt(i**2 + j**2) <= view_radius:
                # Evaulate ray from origin to end point
                # Goal is to determine if the end point can be seen/ evaluated
                line = Ray(agent_loc, (j+agent_loc[0], i+agent_loc[1]))

                # Visualise points the agent can see 
                if line.check_view_v2(obstacles):
                    # Point can be seen
                    points_in_vision.append((j+agent_loc[0],i+agent_loc[1]))

    if DEBUG:
        
        fig, ax = plt.subplots()

        r = view_radius

        for i in range(-r,r+1):
            for j in range(-r,r+1):
                if i == 0 and j == 0:
                    
                    plt.scatter(agent_loc[1],agent_loc[0],color='c')
                
                elif math.sqrt(i**2 + j**2) <= r:
                    # Evaulate ray from origin to end point
                    # Goal is to determine if the end point can be seen/ evaluated

                    line = Ray(agent_loc, (j+agent_loc[0], i+agent_loc[1]))

                    # Visualise points the agent can see 
                    if line.check_view_v2(obstacles):
                        # Point can be seen
                        ax.scatter(i+agent_loc[1], j+agent_loc[0],color='b')
                    else:
                        # Point cannot be seen
                        ax.scatter(i+agent_loc[1], j+agent_loc[0],color='r')

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

    
    return points_in_vision

if __name__ == "__main__":
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
    obstacles = [(5,0), (6,0), (7,0), (6,1), (6,2), (3,-1), (3,0), (3,1), (3,2), (3,4), (3,5), (5,5), (6,5)]

    # Timestep
    t = 0

    # Locations
    locations = [agent[t] for agent in agents]
    
    # View distance
    r = 4

    res = fov(0, locations, r)
    print(res)

    res = fov_blocking(0, locations, r, obstacles, DEBUG=True)
    print(res)

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

        rect = plt.Rectangle((obstacle[1]-0.5, obstacle[0]-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='none')
        ax.add_patch(rect)

    fig.gca().invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    plt.legend()
    plt.show()

    # Script with obstacle blockage
    
    # Main agent
    agent = (5,1)   # (y,x)

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
                if line.check_view_v2([Box(obstacle) for obstacle in obstacles]):
                    # Point can be seen
                    ax.scatter(i+agent[1], j+agent[0],color='b')
                else:
                    # Point cannot be seen
                    ax.scatter(i+agent[1], j+agent[0],color='r')

    # Visualise objects
    for obstacle in obstacles:

        rect = plt.Rectangle((obstacle[1]-0.5, obstacle[0]-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='none')
        ax.add_patch(rect)

    fig.gca().invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    legend_elements = [mline.Line2D([0], [0], marker='o', color='w', label='Agent',markerfacecolor='c', markersize=7),
                       mline.Line2D([0], [0], marker='o', color='w', label='Observable',markerfacecolor='b', markersize=7),
                       mline.Line2D([0], [0], marker='o', color='w', label='Not observable',markerfacecolor='r', markersize=7)]
    ax.legend(handles=legend_elements)
    plt.show()