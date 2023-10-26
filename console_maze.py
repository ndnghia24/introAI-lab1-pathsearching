import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time

import os
from blind_algorithms.ucs import ucs
from blind_algorithms.dfs import dfs
from blind_algorithms.bfs import bfs
from blind_algorithms.a_star import a_star
from blind_algorithms.gbfs import gbfs

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

def print_maze_result(maze, path, shortest_path_cost, expanded_nodes):
    maze_clone = maze.copy()

    for unfinish_path in expanded_nodes:
        # pause for 1 second
        # clear console
        time.sleep(0.005)
        if unfinish_path is not None:
            unfinish_path.pop(0)
            for node in unfinish_path:
                x, y = node
                maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]

        os.system('cls')
        print(f"Min Path Weight SG: {shortest_path_cost}")
        print("Path:")
        for line in maze_clone:
            print(line)
            

    if path is not None:
        path.pop(0)
        path.pop(-1)
        for node in path:
            x, y = node
            maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]

        os.system('cls')
        print(f"Min Path Weight SG: {shortest_path_cost}")
        print("Path:")
        for line in maze_clone:
            print(line)
    else:
        print("No path from S to G.")

    return maze_clone

def print_empty_maze(maze):
    maze_clone = maze.copy()
    for line in maze_clone:
        print(line)

def maze_path_visualize(maze, path, cost):
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
                ax.plot(x, y, marker="o", markersize=10, color="green")

    ax.set_title("Cost: {0}".format(cost))
    plt.show()


def find_path(algo, maze, start, goal, heuristic=None):
    path, cost, expanded_nodes = algo(maze, start, goal, heuristic)

    maze_clone = print_maze_result(maze, path, cost, expanded_nodes)

    def count_expanded_nodes(maze_clone):
        count = 0
        for line in maze_clone:
            for char in line:
                if char != ' ' and char != 'x':
                    count += 1
        return count

    count = count_expanded_nodes(maze_clone)
    print("Expanded Nodes: ", count)
    # maze_path_visualize(maze, path, cost)


#################### MAIN ####################
if __name__ == "__main__":
    # input maze
    maze_path = str(os.path.dirname(os.path.abspath(__file__))) + "\input\level_1\input1.txt"

    # load maze, tìm điểm đầu cuối và danh sách điểm thưởng
    maze, mapping_bonus = load_maze(maze_path)

    start, goal = find_start_goal(maze)

    # A* với heuristic là khoảng cách Manhattan
    
    # find_path(dfs, maze, start, goal)
    # find_path(bfs, maze, start, goal)
    # find_path(ucs, maze, start, goal)
    # find_path(gbfs, maze, start, goal, 1)
    # find_path(gbfs, maze, start, goal, 2)
    # find_path(a_star, maze, start, goal, 2)
    find_path(a_star, maze, start, goal, 2)
