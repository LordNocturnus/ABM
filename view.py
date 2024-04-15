import matplotlib.pyplot as plt  # type: ignore
import matplotlib.lines as mline  # type: ignore
import numpy as np  # type: ignore
import math


def fov(agent: tuple[int, int], view_radius: int, my_map: np.ndarray[int]) -> list[tuple[int, int]]:
    """
    Fov generates a list containing coordinate values indicating which agents, the specified agent 
    x can view, while ignoring obstacles. Here each coordinate represent the following:
    (y-coordinate, x-coordinate) of the points agent x can view
    
    Example case: 
        - view.fov((0,0), 1, ~) -> [(1,0), (0,1), (-1,0), (0,-1)]. 
        The agent located at (0,0) with view_radius 1 can seen 4 points 
    
    Parameters
    ----------
    agent : tuple[int, int]
        Location of the agent within the map, specified as (y, x)
    
    view_radius : int
        maximum unrestricted view range of the agent
    
    my_map : np.ndarray
        Map provided as numpy array where 1 indicates a wall and zero indicates free space

    Returns
    -------
    list[tuple[int, int]]
        A list of coordinate values indicating which agents, agent `agent` can view within the map. 
        The agent cannot sea itself, is a feature implemented by default within the program. 

    Raises
    ------
    None
    """

    points_in_vision = []

    # Store the location of the obstacles as tuples in a list
    obstacles = [tuple(el) for el in np.argwhere(my_map == 1)]
    
    for i in range(-view_radius, view_radius+1):
        for j in range(-view_radius, view_radius+1):
            
            # Agent own location is defined as cannot be seen
            if i == 0 and j == 0:
                continue
            
            # Check if the point is within view radius of the agent
            elif math.sqrt(i**2 + j**2) <= view_radius:
                
                point = (agent[0] + j, agent[1] + i)

                if point not in obstacles:
                    
                    points_in_vision.append(point)

    return points_in_vision


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
        self.reso = 50

        self.start_x = start[1]
        self.start_y = start[0]
        self.end_x = end[1]
        self.end_y = end[0]
        self.slope = math.atan2(self.end_y - self.start_y, self.end_x - self.start_x)

    
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

    ## ---------------------------------------------------------------------------------------------------
    ##  Uncomment lines below, and set DEBUG to true to enable the generation of plots of the agent view.
    ## ---------------------------------------------------------------------------------------------------
    # if DEBUG:
        
    #     fig, ax = plt.subplots()

    #     r = view_radius

    #     for i in range(-r,r+1):
    #         for j in range(-r,r+1):
    #             if i == 0 and j == 0:
                    
    #                 plt.scatter(agent_loc[1],agent_loc[0],color='c')
                
    #             elif math.sqrt(i**2 + j**2) <= r:
    #                 # Evaulate ray from origin to end point
    #                 # Goal is to determine if the end point can be seen/ evaluated

    #                 line = Ray(agent_loc, (j+agent_loc[0], i+agent_loc[1]))

    #                 # Visualise points the agent can see 
    #                 if line.check_view_v2(obstacles):
    #                     # Point can be seen
    #                     ax.scatter(i+agent_loc[1], j+agent_loc[0],color='b')
    #                 else:
    #                     # Point cannot be seen
    #                     ax.scatter(i+agent_loc[1], j+agent_loc[0],color='r')

    #     # Visualise objects
    #     for obstacle in obstacles:

    #         rect = plt.Rectangle((obstacle.x-0.5, obstacle.y-0.5), 1, 1, linewidth=1, edgecolor='k', facecolor='none')
    #         ax.add_patch(rect)
    #     # plt.scatter(agent[1],agent[0],color='c')

    #     fig.gca().invert_yaxis()
    #     ax.set_aspect('equal', adjustable='box')
    #     legend_elements = [mline.Line2D([0], [0], marker='o', color='w', label='Agent',markerfacecolor='c', markersize=7),
    #                     mline.Line2D([0], [0], marker='o', color='w', label='Observable',markerfacecolor='b', markersize=7),
    #                     mline.Line2D([0], [0], marker='o', color='w', label='Not observable',markerfacecolor='r', markersize=7)]
    #     ax.legend(handles=legend_elements)
    #     plt.show()

    
    return points_in_vision

if __name__ == "__main__":

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
