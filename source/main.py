import subprocess
import os

# get current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))
mother_dir = os.path.dirname(current_dir)

# Specify the arguments to be passed to pygame_maze.py
arguments = [
    "python", os.path.join(current_dir, "pygame_maze.py"),
    "--maze", os.path.join(mother_dir, "input\\level_1\\input1.txt"),
    "--algorithm", "a_star",
    "--heuristic", "heuristic_manhattan",
    "--visualize", "True"
]

algorithm = ["dfs", "bfs", "ucs", "gbfs", "a_star"]

print(arguments[3], arguments[5], arguments)

for root, dirs, files in os.walk(os.path.join(mother_dir, "input")):
    for file in files:
        # Get the input file path
        input_path = os.path.join(root, file)
        arguments[3] = input_path
        # Loop through all the algorithms
        for algo in algorithm:
            arguments[5] = algo
            if algo == "a_star" or algo == "gbfs":
                arguments[7] = "heuristic_manhattan"
                subprocess.run(arguments)
                arguments[7] = "heuristic_euclidean"
                subprocess.run(arguments)
            else:
                arguments[7] = ""
                subprocess.run(arguments)
