import subprocess
import os

# get current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))
mother_dir = os.path.dirname(current_dir)

# Specify the arguments to be passed to pygame_maze.py
arguments = [
    "python3", os.path.join(current_dir, "pygame_noBonus_maze.py"),
    "--maze", os.path.join(mother_dir, "input/level_1/input1.txt"),
    "--algorithm", "ucs",
    "--heuristic", "",
    "--visualize", "True"
]

# normal maze
algorithm = ["dfs", "bfs", "ucs", "gbfs", "a_star"]

for root, dirs, files in os.walk(os.path.join(mother_dir, "input/level_1")):
    for file in files:
        arguments[1] = os.path.join(current_dir, "pygame_noBonus_maze.py")
        # Get the input file path
        input_path = os.path.join(root, file)
        arguments[3] = input_path
        # Loop through all the algorithms
        for algo in algorithm:
            arguments[5] = algo
            if algo == "a_star" or algo == "gbfs":
                arguments[7] = "1"
                subprocess.run(arguments)
                arguments[7] = "2"
                subprocess.run(arguments)
            else:
                arguments[7] = ""
                subprocess.run(arguments)

# half bonus maze
for root, dirs, files in os.walk(os.path.join(mother_dir, "input/level_2")):
    for file in files:
        arguments[1] = os.path.join(current_dir, "pygame_halfBonus_maze.py")
        # Get the input file path
        input_path = os.path.join(root, file)
        arguments[3] = input_path
        arguments[5] = "bonus"
        arguments[7] = ""
        subprocess.run(arguments)

# full bonus maze
for root, dirs, files in os.walk(os.path.join(mother_dir, "input/level_3")):
    for file in files:
        arguments[1] = os.path.join(current_dir, "pygame_fullBonus_maze.py")
        # Get the input file path
        input_path = os.path.join(root, file)
        arguments[3] = input_path
        arguments[5] = "find_path_with_diem_don"
        arguments[7] = ""
        subprocess.run(arguments)


# teleport maze
for root, dirs, files in os.walk(os.path.join(mother_dir, "input/advance")):
    for file in files:
        arguments[1] = os.path.join(current_dir, "pygame_teleport_maze.py")
        # Get the input file path
        input_path = os.path.join(root, file)
        arguments[3] = input_path
        arguments[5] = "ucs_teleport"
        arguments[7] = ""
        subprocess.run(arguments)
