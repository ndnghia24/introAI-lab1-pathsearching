import pygame
import argparse
import imageio
import os
import numpy as np

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
    maze_path = os.path.join(maze_path)
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
LIGHT_GREEN = (0, 245, 0)


def print_maze_result(maze, output_path, path, shortest_path_cost, expanded_nodes, visualize=None):

    start, goal = find_start_goal(maze)

    def draw_maze(screen, maze):
        maze_width = len(maze[0])
        maze_height = len(maze)
        cell_size = 30
        padding = cell_size*0.05

        for y in range(len(maze)):
            for x in range(len(maze[y])):
                cell = maze[y][x]
                COLOR = BLACK
                if (x, y) == start:
                    COLOR = RED
                elif (x, y) == goal:
                    COLOR = BLUE
                elif cell == ' ':
                    COLOR = WHITE
                elif cell == '█':
                    COLOR = RED
                elif cell == '▒':
                    COLOR = ORANGE
                elif cell == '+':
                    COLOR = LIGHT_GREEN

                pygame.draw.rect(screen, COLOR, (x * cell_size + padding, y * cell_size + padding, cell_size- 2*padding, cell_size- 2*padding))
    
        pygame.display.update()

    maze_clone = maze.copy()
    maze_width = len(maze_clone[0])
    maze_height = len(maze_clone)
    cell_size = 30

    if visualize == "False" or visualize == "false" or visualize == None:
        for unfinish_path in expanded_nodes:
            for node in unfinish_path:
                x, y = node
                if node == start or node == goal:
                    continue
                maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]
        if path is not None:
            for node in path:
                x, y = node
                if node == start or node == goal:
                    continue
                maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]
    else:
        # Khởi tạo Pygame
        pygame.init()
        # Lưu ảnh từng bước tìm kiếm để render video
        images_list = []

        # Kích thước cửa sổ Pygame
        window_width = maze_width * cell_size
        window_height = maze_height * cell_size
        screen = pygame.display.set_mode((window_width, window_height))
        
        draw_maze(screen, maze_clone)
        for i in range(30):
            images_list.append(np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface()), 1)))

        for unfinish_path in expanded_nodes:
            for node in unfinish_path:
                x, y = node
                if node == start or node == goal or maze_clone[y][x] == '+':
                    continue
                maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]
            draw_maze(screen, maze_clone)
            images_list.append(np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface()), 1)))

            # pygame.time.delay(5)  # Delay for 5 milliseconds

        if path is not None:
            for node in path:
                x, y = node
                if node == start or node == goal or maze_clone[y][x] == '+':
                    continue
                maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]
                draw_maze(screen, maze_clone)

        for i in range(30):
            images_list.append(np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface()), 1)))

        # Lưu video
        imageio.mimsave(output_path + ".mp4", images_list, fps=30, quality=5, codec="libx264", pixelformat="yuv420p")
        
        pygame.quit()

    return maze_clone


def find_path(algo, maze, output_path, start, goal, heuristic=None, visualize=None):
    path, cost, expanded_nodes, runtime = algo(maze, start, goal, heuristic)

    if (cost is None):
        return None, None, None

    maze_clone = print_maze_result(maze, output_path, path, cost, expanded_nodes, visualize)

    def count_expanded_nodes(maze_clone):
        count = 0
        for line in maze_clone:
            for char in line:
                if char != ' ' and char != 'x':
                    count += 1
        return count

    expanded_nodes_counter = count_expanded_nodes(maze_clone)

    return cost, expanded_nodes_counter, runtime * 1000 # convert from s to ms

#################### MAIN ####################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Maze Solver')
    parser.add_argument('--maze', type=str, 
                        required=True,
                        help='Path to the maze file')
    parser.add_argument('--algorithm', type=str, 
                        required=True,
                        choices=['dfs', 'bfs', 'ucs', 'gbfs', 'a_star'], help='Search algorithm to use')
    parser.add_argument('--heuristic', type=str, 
                        default='',
                        choices=['','1', '2'], help='Heuristic for GBFS and A*')
    parser.add_argument('--visualize', type=str, 
                        default='False',
                        choices=['True', 'False'], help='Visualize the search process in PyGame')

    args = parser.parse_args()

    # input/level_1/input1.txt
    input_path = args.maze
    algorithm = args.algorithm
    heuristic = args.heuristic

    # custom output heuristic path extention
    if heuristic != "":
        output_path = os.path.join(input_path.replace("input/", "output/").split(".")[0], algorithm + "_heuristic_" + str(heuristic))
    else:
        output_path = os.path.join(input_path.replace("input/", "output/").split(".")[0], algorithm)
    output_path = os.path.join(output_path)

    # Create output path
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    output_path = os.path.join(output_path, algorithm)

    # Load maze, find start and goal, and call the appropriate search algorithm
    maze, mapping_bonus = load_maze(args.maze)
    start, goal = find_start_goal(maze)

    if args.algorithm == 'dfs':
        cost, expanded_nodes_counter, runtime = find_path(dfs, maze, output_path, start, goal, visualize=args.visualize)
    elif args.algorithm == 'bfs':
        cost, expanded_nodes_counter, runtime = find_path(bfs, maze, output_path, start, goal, visualize=args.visualize)
    elif args.algorithm == 'ucs':
        cost, expanded_nodes_counter, runtime = find_path(ucs, maze, output_path, start, goal, visualize=args.visualize)
    elif args.algorithm == 'gbfs':
        cost, expanded_nodes_counter, runtime = find_path(gbfs, maze, output_path, start, goal, heuristic=args.heuristic, visualize=args.visualize)
    elif args.algorithm == 'a_star':
        cost, expanded_nodes_counter, runtime = find_path(a_star, maze, output_path, start, goal, heuristic=args.heuristic, visualize=args.visualize)

    """# Write the result to a text file
    with open(output_path + "_detail.txt", "w") as file:
        file.write("Cost: " + str(cost) + "/n")
        file.write("Expanded Nodes: " + str(expanded_nodes_counter) + "/n")
        file.write("Runtime: " + str(runtime) + " ms/n")"""

    with open(output_path + ".txt", "w") as file:
        if (cost is not None):
            file.write(str(cost))
        else:
            file.write("NO")


    #### Example of how to call the search algorithms ####
    # > python source/pygame_maze.py --maze input/level_1/input1.txt --algorithm a_star --heuristic 1 --visualize True
