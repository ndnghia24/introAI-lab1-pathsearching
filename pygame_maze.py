import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pygame
import time
import sys

import os
from Algorithms.ucs import ucs
from Algorithms.dfs import dfs
from Algorithms.bfs import bfs
from Algorithms.a_star import a_star
from Algorithms.gbfs import gbfs

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

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

def print_maze_result(maze, path, shortest_path_cost, expanded_nodes):

    def draw_maze(screen, maze):
        maze_width = len(maze[0])
        maze_height = len(maze)
        cell_size = 30
        padding = cell_size*0.05

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                COLOR = BLACK
                if cell == ' ':
                    COLOR = WHITE
                elif cell == '█':
                    COLOR = RED
                elif cell == '▒':
                    COLOR = ORANGE
                elif cell == 'S':
                    COLOR = RED
                elif cell == 'G':
                    COLOR = BLUE

                pygame.draw.rect(screen, COLOR, (x * cell_size + padding, y * cell_size + padding, cell_size- 2*padding, cell_size- 2*padding))
    
        pygame.display.update()


    maze_clone = maze.copy()
    maze_width = len(maze_clone[0])
    maze_height = len(maze_clone)
    cell_size = 30

    # Khởi tạo Pygame
    pygame.init()
    # Kích thước cửa sổ Pygame
    window_width = maze_width * cell_size
    window_height = maze_height * cell_size
    screen = pygame.display.set_mode((window_width, window_height))
    
    for unfinish_path in expanded_nodes:
        draw_maze(screen, maze_clone)
        pygame.time.delay(5)  # Delay for 5 milliseconds
        for node in unfinish_path:
            x, y = node
            if maze_clone[y][x] == 'S' or maze_clone[y][x] == 'G':
                continue
            maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]

    if path is not None:
        for node in path:
            x, y = node
            if maze_clone[y][x] == 'S' or maze_clone[y][x] == 'G':
                continue
            maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]

    draw_maze(screen, maze_clone)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    return maze_clone


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
    find_path(ucs, maze, start, goal)
    # find_path(gbfs, maze, start, goal, 1)
    # find_path(gbfs, maze, start, goal, 2)
    # find_path(a_star, maze, start, goal, 2)
    # find_path(a_star, maze, start, goal, 2)
