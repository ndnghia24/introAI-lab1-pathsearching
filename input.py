import os

# lưu danh sách điểm thưởng, điểm đón
mapping_dict = {}

# lưu đường dẫn file maze
maze_path = str(os.path.dirname(os.path.abspath(__file__))) + "\input\level_1\input1.txt"

with open(maze_path, "r") as file:
    n = int(file.readline())

    for i in range(n):
        buff = file.readline()
        coordinates = buff.split(" ")
        
        x = int(coordinates[0])
        y = int(coordinates[1])
        val = int(coordinates[2])

        mapping_dict[(x, y)] = val

    data = [line.rstrip() for line in file.readlines()]

for i in data:
    print(i)