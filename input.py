import os

maze_path = str(os.path.dirname(os.path.abspath(__file__))) + "\input\level_1\input1.txt"

with open(maze_path, "r") as file:
    data = [line.rstrip() for line in file.readlines()]

for i in data:
    print(i)