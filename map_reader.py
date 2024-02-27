import map_gen

def setup_scenario(map: str) -> tuple:
    """
    File reader which loads the specified map and coverts into useable structure for the program

    Generic file reader based on original reader within run_experiments.py

    Args:
        param1: (string) Containts the full map content, where agent start and end locations are specified:
        example:
            4 7             # grid with 4 rows and 7 columns
            @ @ @ @ @ @ @   # example row with obstacle in every column
            @ . . . . . @   # example row with 5 free cells in the middle
            @ @ @ . @ @ @
            @ @ @ @ @ @ @
            2               # 2 agents in this experiment
            1 1 1 5         # agent 1 starts at (1,1) and has (1,5) as goal
            1 2 1 4         # agent 2 starts at (1,2) and has (1,4) as goal

    Returns:
        tuple:
            param1: (array) map loaded where walls (@) are converted to True and wakable 
            locations (.) are converted to False. The array has the size equal to the first 
            input line in the specified configuration file of the map.

            param2: (array) Start positions of the various agents in the map (x, y)

            param3: (array) Goal location for the various agents in the map (x, y)

    Raises:
        BaseException: Bad map detected, inconsistent size , or impossible placement of agents
    """
    my_map: list[list[bool]] = []
    starts: list[int] = []
    goals: list[int] = []

    file = map.splitlines()

    line = 0
    
    dimension_map = [int(el) for el in file[line].split(" ")]
    my_map_str = "\n".join(file[1:dimension_map[0]+1])

    line += 1

    for row in range(dimension_map[0]):

        row_map = file[line + row].split(" ")
        row_map = [True if el == "@" else False for el in row_map]
        my_map.append(row_map)

    # Sanity check \\ mainly ensuring the size is okay

    for id, content in enumerate(my_map, start=1):

        if len(content) != dimension_map[1]:
            print(my_map_str)
            raise BaseException(f"The map has unequaly dimensions between lines. Detected on line: {id}")
    
    line += dimension_map[0]

    agent_amount = int(file[line])

    line += 1

    for id, agent in enumerate(range(agent_amount), start=1):
        
        sx, sy, gx, gy = [int(x) for x in file[line + agent].split(' ')]
        starts.append((sx, sy))
        goals.append((gx, gy))

        # Agent init located on invalid location
        if my_map[sy][sx] == True:
            raise BaseException(f"Agent_init {id} is located on invalid location")
        # Agent goal located on invalid location
        if my_map[gy][gx] == True:
            raise BaseException(f"Agent_goal {id} is located on invalid location")
    
    return my_map, starts, goals


if __name__ == "__main__":
    map = "maps/assignment_1.map"
    test_map_1 = map_gen.MapGenerator(map)
    file = test_map_1.generate()

    config = setup_scenario(file)
