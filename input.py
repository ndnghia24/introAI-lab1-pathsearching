import os

# lưu danh sách điểm thưởng, điểm đón
mapping_bonus = {}

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

        mapping_bonus[(x, y)] = val

    data = [line.rstrip() for line in file.readlines()]

# kiểm tra vị trí bắt đầu và đích
start = None
goal = None
for i in range(len(data)):
    for j in range(len(data[i])):
        if data[i][j] == 'S':
            start = (i, j)
        elif data[i][j] == 'G':
            goal = (i, j)

if start == None or goal == None:
    print("Không tìm thấy Start và Goal")
else:
    for i in data:
        print(i)