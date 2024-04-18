import run_experiments
import collisions

from cbs import CBSSolver
from independent import IndependentSolver
from prioritized import PrioritizedPlanningSolver
from distributed import DistributedPlanningSolver
from visualize import Animation

# Map: my_map
my_map = "instances\hypotheses\hypothesis_1.txt"
print(f"==> Solving: {my_map} using prioritized <==")

# Solve 
my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])

animation = Animation(my_map_arr, starts, goals, paths)
animation.show()

print(f"Cost of the found solution {len(paths[-1])}")

# Map: my_map
my_map = "instances\hypotheses\hypothesis_2.txt"
print(f"==> Solving: {my_map} using prioritized <==")

# Solve 
my_map_arr, starts, goals = run_experiments.import_mapf_instance(my_map)
paths = PrioritizedPlanningSolver(my_map_arr, starts, goals, printing = False).find_solution([])

animation = Animation(my_map_arr, starts, goals, paths)
animation.show()

print(f"Cost of the found solution {len(paths[-1])}")