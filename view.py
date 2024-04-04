import matplotlib.pyplot as plt  # type: ignore
import matplotlib.lines as mline  # type: ignore
import numpy as np  # type: ignore
import math

# def generate_view_map() -> dict[list[tuple[int,int]]]:
    
#     view_map = {}

#     # Evaluate view for all posible locations Precomp step, to reduce computational requirements. 
#     view_map["y", "x"] = agent_vision()
    
#     return view_map

def fov(m_id: int, locations: list[tuple[int, int]], view_radius: int) -> list[bool]:
    """
    Fov generates a list containing boolean values indicating which agents, the specified agent 
    x can view, while ignoring obstacles. True indicates the agent can be viewed, while false 
    idicates the agent cannot be observed by agent x.
    
    Example: output [False, False, True, True, False, False], if the agent observing other agents 
    is given index 1, is gives itself the default value False (cannot see iteself). It can however see
    agent 2 and 3 (assigned true), and cannot observe agent 0, 1, 4, 5 (assigned False).
    
    Parameters
    ----------
    m_id : int
        Index of the main agent, who is observing other agents within the map.
    
    locations : list[tuple[int, int]]
        Locations of all agents supplied as a list of coordinates (y-location:int, x-location:int) 
        at the evaluated timestep.
    
    view_radius : int
        maximum unrestricted view range of the agent

    Returns
    -------
    list[bool]
        A list of boolean values indicating which agents, agent `m_id` can view within the map. Where True means 
        an agent is in view, and false means an agent is not in view. The agent `m_id` assigns itself False.

    Raises
    ------
    None
    """

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


def fov_blocking(agent: tuple[int, int], view_radius: int,
                 my_map: np.ndarray[int], DEBUG: bool=False) -> list[tuple[int, int]]:
    """
    Fov_blocking generates a list containing the coordinate values indicating which positions, 
    the specified agent can view, considering obstacles. The coordinates are supplied as 
    [(y, x), (y, x), (y, x), (y, x), ...]
    
    Example: output for agent located at (1,1) view view-radius 2
    -------------------------------------------------------------

    my_map:
        . . . .
        . 0 @ .
        . @ @ .
        . . . .

    output: [(1, -1), (0, 0), (1, 0), (2, 0), (-1, 1), (0, 1), (0, 2)]
    

    Methode: Basic version ray evaluation code, which evaluated rays going to all possible points within 
    the unrestricted view of the agent. By then evaulating if the ray intersetcs with an obstacle it can be 
    determined if that location can be viewed or not. Geomteric formulation for checking intersection was 
    based on: https://stackoverflow.com/a/4977569
    
    Parameters
    ----------
    agent : tuple[int, int]
        Location of the agent within the map, specified as (y, x)
    
    view_radius : int
        maximum unrestricted view range of the agent
    
    my_map : np.ndarray
        Map provided as numpy array where 1 indicates a wall and zero indicates free space

    DEBUG (optional, default False) : bool
        True, Enables plotting functionality to view the agents' view  

    Returns
    -------
    list[tuple[int, int]]
        A list containing the points the secified `agent` can view within the specified `my_map`.
        Provided as [(y,x), (y,x), ...]

    Raises
    ------
    None
    """

    obstacles = [Box(el) for el in np.argwhere(my_map == 1)]

    view_map = agent_vision(agent, view_radius, obstacles, DEBUG)

    return view_map


class Box:
    """
    A box object, required for the ray intersection implmentation. It functions as an object 
    representation of the various obstacles within the map. To create an obstacle the following 
    code is used: `Box((10, 5))`. This creates the box object for the obstacle located at y = 10 
    and x = 5.

    Attributes
    ----------
        self.x : int
            x location of the obstacle
        self.y : int
            y location of the obstacle
    
    Methodes
    --------
        bounds
            list[list[tuple[int, int]]]
            returns the coordinates representing the lines segements representing to bounds of the 
            square shaped obstacle.  
    """

    def __init__(self, location: tuple[int,int]) -> None:
        """
        Initliase the object

        Parameters
        ----------
        locations : tuple[int, int]
            Location of the obstacle supplied as (y-location, x-location)
        
        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.x = location[1]
        self.y = location[0]
        self.segments = self.bounds
    
    @property
    def bounds(self) -> list[list[tuple[float, float]]]:
        """
        returns the coordinates representing the lines segements representing to bounds of the 
        square shaped obstacle.  

        Parameters
        ----------
        None

        Returns
        -------
        locations : tuple[int, int]
            Location of the obstacle supplied as (y-location, x-location)

        Raises
        ------
        None
        """
        padding = 0.49
        out = [[(self.y + padding, self.x + padding), (self.y + padding, self.x - padding)],
               [(self.y + padding, self.x + padding), (self.y - padding, self.x + padding)],
               [(self.y - padding, self.x - padding), (self.y - padding, self.x + padding)],
               [(self.y - padding, self.x - padding), (self.y + padding, self.x - padding)]]
        return out


class Ray:
    """
    A ray object going from the agent location to another specified location within the grid. Required to
    analyse if the agent can view another point within its environment.

    Attributes
    ----------
        self.start_x : int
            x location of vertex starting location
        self.start_y : int
            y location of vertex starting location
        self.end_x : int
            x location of vertex ending location
        self.end_y : int
            y location of vertex ending location
    
    Methodes
    --------
        check_view_v2(obstacles)
            bool
            returns False if the ray is blocked by any obstacle else True is returend
    """

    def __init__(self, start: tuple[int, int], end: tuple[int, int]) -> None:
        """
        Initliase the Ray object

        Parameters
        ----------
        start : tuple[int, int]
            (y, x) location of vertex starting location

        end : tuple[int, int]
            (y, x) location of vertex starting location
        
        Returns
        -------
        None

        Raises
        ------
        None
        """
        self.start_x = start[1]
        self.start_y = start[0]
        self.end_x = end[1]
        self.end_y = end[0]

    def check_view(self, obstacles: list[Box]) -> bool:
        
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
    
    def check_view_v2(self, obstacles: list[Box]) -> bool:
        """
        Check if the ray intersects with any obstacles.

        Parameters
        ----------
        obstacles : list[Box]
            List containing the Box objects within the environment
        
        Returns
        -------
        bool
            True if ray does not intersect with any obstacles within the environment. Else False

        Raises
        ------
        None
        """
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


def agent_vision(agent_loc: tuple[int, int], view_radius: int, obstacles: list[Box], 
                 DEBUG: bool=False) -> list[tuple[int, int]]:
    """
    Returns the points the agent can be view based on the its view radius, the obstacles and the agents within 
    the environment. 

    Parameters
    ----------
    agent_loc : tuple[int, int]
        The agent location provided as (y-location, x-location)
    
    view_radius : int
        maximum unrestricted view range of the agent
    
    obstacle_locations : list[Box]
        Locations of all obstacles within the map supplied as a list of Box objects.

    DEBUG (optional, default False) : bool
        True, Enables plotting functionality to view the agents' view
    
    Returns
    -------
    list[tuple[int, int]]
        Returns list of all point the agent can view, point is list are stored as (y-location, x-location)

    Raises
    ------
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
    # # Helper functions 
    # get_y = lambda coords: [loc[0] for loc in coords]
    # get_x = lambda coords: [loc[1] for loc in coords]

    # # Agents [(y,x), (y,x), (y,x)]
    # agent1 = [(0,0), (0,1), (0,2), (1,2), (2,2)]
    # agent2 = [(1,1), (1,2), (1,3), (2,3), (2,2)]
    # agent3 = [(5,1), (5,2), (5,3), (6,3), (6,4)]
    # agent4 = [(7,1), (7,2), (7,3), (7,4), (7,5)]

    # # All agents for evaluation 
    # agents = [agent1, agent2, agent3, agent4]
    # colors = ['r','c','b','g']

    # # Obstacles
    # obstacles = [(5,0), (6,0), (7,0), (6,1), (6,2), (3,-1), (3,0), (3,1), (3,2), (3,4), (3,5), (5,5), (6,5)]

    # # Timestep
    # t = 0

    # # Locations
    # locations = [agent[t] for agent in agents]
    
    # # View distance
    # r = 4

    # res = fov(0, locations, r)
    # print(res)

    # res = fov_blocking(0, locations, r, obstacles, DEBUG=True)
    # print(res)

    # fig, ax = plt.subplots()

    # ### VISUALISATION ###
    # # Visualise paths
    # for id, agent in enumerate(agents):

    #     ax.plot(get_x(agent), get_y(agent), label=f"Agent #{id}")
        
    #     for loc in agent:
    #         circle = plt.Circle((loc[1], loc[0]), r, color=colors[id], alpha=0.2, fill=False)
    #         ax.add_patch(circle)

    # # Visualise objects
    # for obstacle in obstacles:

    #     rect = plt.Rectangle((obstacle[1]-0.5, obstacle[0]-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='none')
    #     ax.add_patch(rect)

    # fig.gca().invert_yaxis()
    # ax.set_aspect('equal', adjustable='box')
    # plt.legend()
    # plt.show()

    env = np.array([[0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0]])
    
    res = fov_blocking((0,0), 2, env, DEBUG=True)
    print(res)

    env = np.array([[0,0,0,0],
                    [0,0,1,0],
                    [0,1,1,0],
                    [0,0,0,0]])
    
    res = fov_blocking((1,1), 2, env, DEBUG=True)
    print(res)

