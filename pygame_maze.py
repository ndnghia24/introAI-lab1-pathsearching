import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pygame
import argparse


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
    maze_path = os.path.join(os.path.dirname(__file__), maze_path)
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
    
    draw_maze(screen, maze_clone)
    pygame.image.save(screen, "before.png")

    for unfinish_path in expanded_nodes:
        for node in unfinish_path:
            x, y = node
            if maze_clone[y][x] == 'S' or maze_clone[y][x] == 'G':
                continue
            maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]
        draw_maze(screen, maze_clone)
        pygame.time.delay(5)  # Delay for 5 milliseconds

    if path is not None:
        for node in path:
            x, y = node
            if maze_clone[y][x] == 'S' or maze_clone[y][x] == 'G':
                continue
            maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]

    draw_maze(screen, maze_clone)
    pygame.image.save(screen, "after.png")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
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
    print("Path Cost: ", cost)
    print("Expanded Nodes: ", count)
    print("Runtime: ", runtime*1000)
    # write cost and count to file
    with open("output.txt", "w") as file:
        file.write("Cost: " + str(cost) + "\n")
        file.write("Expanded Nodes: " + str(count) + "\n")
        file.write("Runtime: " + str(runtime*1000) + "\n")
    # maze_path_visualize(maze, path, cost)


#################### MAIN ####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Maze Solver')
    parser.add_argument('--maze', type=str, 
                        default='input\level_1\input1.txt',
                        help='Path to the maze file')
    parser.add_argument('--algorithm', type=str, 
                        default='dfs', 
                        choices=['dfs', 'bfs', 'ucs', 'gbfs', 'a_star'], help='Search algorithm to use')
    parser.add_argument('--heuristic', type=str, 
                        default='heuristic_manhattan', 
                        choices=['heuristic_manhattan', 'heuristic_euclidean'], help='Heuristic for GBFS and A*')

    args = parser.parse_args()

    # Load maze, find start and goal, and call the appropriate search algorithm
    maze, mapping_bonus = load_maze(args.maze)
    start, goal = find_start_goal(maze)

    if args.algorithm == 'dfs':
        find_path(dfs, maze, start, goal)
    elif args.algorithm == 'bfs':
        find_path(bfs, maze, start, goal)
    elif args.algorithm == 'ucs':
        find_path(ucs, maze, start, goal)
    elif args.algorithm == 'gbfs':
        find_path(gbfs, maze, start, goal, args.heuristic)
    elif args.algorithm == 'a_star':
        find_path(a_star, maze, start, goal, args.heuristic)
