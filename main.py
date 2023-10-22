import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import os
from algorithms.ucs import ucs
from algorithms.dfs import dfs
from algorithms.a_star import a_star

def find_start_goal(maze):
    # Tìm vị trí S và G trong ma trận
    start = None
    goal = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (j, i)
            elif maze[i][j] == 'G':
                goal =  (j, i)
    return start, goal


def load_maze(maze_path):
    # lưu điểm thưởng 
    mapping_bonus = {}
    # đọc file maze
    try:
        with open(maze_path, "r") as file:
            n = int(file.readline())
            for i in range(n):
                buff = file.readline()
                coordinates = buff.split(" ")
              
                x = int(coordinates[0])
                y = int(coordinates[1])
                val = int(coordinates[2])

                mapping_bonus[(x, y)] = val
            maze = [line.rstrip() for line in file.readlines()]      
        return maze, mapping_bonus
        
    except FileNotFoundError:
        print("Không tìm thấy file maze")
        exit()

def print_maze_result(maze, path, shortest_path_cost):
    maze_clone = maze.copy()
    if path is not None:
            print(f"Min Path Weight SG: {shortest_path_cost}")
            print("Path:")
            path.pop(0)
            path.pop(-1)
            for node in path:
                x, y = node
                maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]
            for line in maze_clone:
                print(line)
    else:
        print("No path from S to G.")


def maze_path_visualize(maze, path):
    rows = len(maze)
    cols = len(maze[0])

    # Tạo bản đồ màu tùy chỉnh
    cmap = mcolors.ListedColormap(["black", "white", "red", "yellow", "purple", "cyan", "lightblue"])
    fig, ax = plt.subplots(figsize=(cols, rows))
    colored_maze = [[6 if cell != "x" else 0 for cell in row] for row in maze]
    ax.imshow(colored_maze, cmap=cmap, origin="upper")
    ax.axis("off")

    # Vẽ đường đi
    if path:
        path_x, path_y = zip(*path)
        ax.plot(path_x, path_y, color="red", linewidth=2)

    # Vẽ điểm đầu và cuối
    start = None
    end = None
    for y in range(rows):
        for x in range(cols):
            if maze[y][x] == "S":
                ax.plot(x, y, marker="o", markersize=10, color="yellow")
            elif maze[y][x] == "E":
                ax.plot(x, y, marker="o", markersize=10, color="purple")

    ax.set_title("Cost: {0}".format(len(path) + 1))
    plt.show()


def find_path(algo, maze, start, goal, heuristic=None):
    cost, path = algo(maze, start, goal, heuristic)

    print_maze_result(maze, path, cost)
    maze_path_visualize(maze, path)


#################### MAIN ####################
if __name__ == "__main__":

    # input maze
    maze_path = str(os.path.dirname(os.path.abspath(__file__))) + "\input\level_1\input1.txt"

    # load maze, tìm điểm đầu cuối và danh sách điểm thưởng
    maze, mapping_bonus = load_maze(maze_path)
    start, goal = find_start_goal(maze)

    # UCS
    find_path(ucs, maze, start, goal)

    # A* với heuristic là khoảng cách Chebyshev
    find_path(a_star, maze, start, goal, 2)