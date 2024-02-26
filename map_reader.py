def map_reader(map_dir: str) -> tuple:
    """
    File reader which loads the specified map and coverts into useable structure for the program

    Generic file reader based on original reader within run_experiments.py

    Args:
        param1: (string) directory pointing to the map 

    Returns:
        tuple:
            param1: (array) map loaded where walls (@) are converted to False and wakable locations (.) are converted to True
            param2: (tuple) dimension of the map (rows, cols)

    Raises:
        FileNotFound: Exception if the map loaded is not found in the current directory
        BaseException: Bad map detected, inconsistent size
    """
    my_map = []

    try:
        with open(map_dir, "r") as file:
            my_map_str = file.read()    # Local copy for error msg
            file.seek(0)
            for line in file.readlines():
                line = line.rstrip(" \n").split(" ")
                line = [True if el == "@" else False for el in line]
                my_map.append(line)

    except FileNotFoundError:
        raise BaseException(f"{map_dir} doesn't exist")

    # Sanity check \\ mainly ensuring the size is okay
    dimensions = (len(my_map), len(my_map[0]))

    for id, line in enumerate(my_map, start=1):

        if len(line) != dimensions[1]:
            print(my_map_str)
            raise BaseException(f"{map_dir}, has unequaly dimensions between lines detected on line: {id}")

    return my_map, dimensions

def load_agents_data(my_map, agents) -> tuple:
    """
    Load the agents and pass as useable structure for the code, written based on original formulation within run_experiment.py

    Args:
        param1: 

    Returns:
        param1:

    Raises:
        
    """
    starts: list  = []
    goals: list   = []
    
    for id, agent in enumerate(agents, start=1):
        x_pos = int(agent[0])
        y_pos = int(agent[1])

        x_gl = int(agent[2])
        y_gl = int(agent[3])

        # Agent init located on invalid location
        if my_map[y_pos][x_pos] == False:
            raise BaseException(f"Agent_init {id} is located on invalid location")
        # Agent goal located on invalid location
        if my_map[y_gl][x_gl] == False:
            raise BaseException(f"Agent_goal {id} is located on invalid location")
        
        starts.append((x_pos, y_pos))
        goals.append((x_gl,y_gl))

    return starts, goals

if __name__ == "__main__":
    map_reader("testmap.map")