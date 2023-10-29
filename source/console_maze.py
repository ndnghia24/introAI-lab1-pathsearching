import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time

import os
from noBonus_algorithms.ucs import ucs
from noBonus_algorithms.dfs import dfs
from noBonus_algorithms.bfs import bfs
from noBonus_algorithms.a_star import a_star
from noBonus_algorithms.gbfs import gbfs

def find_start_goal(maze):
    # Tìm vị trí S và G trong ma trận
    start = None
    goal = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (j, i)
            elif maze[i][j] == ' ' and (i == 0 or i == len(maze) - 1 or j == 0 or j == len(maze[i]) - 1):
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
        time.sleep(0.01)
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

def find_path(algo, maze, start, goal, heuristic=None):
    path, cost, expanded_nodes, runtime = algo(maze, start, goal, heuristic)

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
    # find_path(gbfs, maze, start, goal, "heuristic_manhattan")
    # find_path(gbfs, maze, start, goal, "heuristic_euclidean")
    # find_path(a_star, maze, start, goal, "heuristic_manhattan")
    find_path(a_star, maze, start, goal, "heuristic_euclidean")
