

class MapGenerator(object):

    def __init__(self, path, agents=7, seed=0):
        with open(path, "r") as file:
            self.map = file.readlines()
