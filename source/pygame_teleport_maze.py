import pygame
import argparse
import imageio
import os
import numpy as np
import random

from teleportation_algorithms.ucs_teleport import ucs_teleport

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
    mapping_teleport = {}
    # đọc file maze
    try:
        with open(maze_path, "r") as file:
            n = int(file.readline())
            for i in range(n):
                buff = file.readline()
                coordinates = buff.split(" ")
              
                x1 = int(coordinates[0])
                y1 = int(coordinates[1])
                x2 = int(coordinates[2])
                y2 = int(coordinates[3])

                mapping_teleport[(x1, y1)] = (x2, y2)
                mapping_teleport[(x2, y2)] = (x1, y1)

            maze = [line.rstrip() for line in file.readlines()]      
        return maze, mapping_teleport
        
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
                RANDOM_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                if (x, y) == start:
                    COLOR = RED
                elif (x, y) == goal:
                    COLOR = BLUE
                elif cell == ' ' or (cell > '0' and cell <= '9'):
                    COLOR = WHITE
                elif cell == '█':
                    COLOR = RED
                elif cell == '▒':
                    COLOR = ORANGE
            
                pygame.draw.rect(screen, COLOR, (x * cell_size + padding, y * cell_size + padding, cell_size- 2*padding, cell_size- 2*padding))

                if cell > '0' and cell <= '9':
                    number = ord(cell) - ord('0')
                    # Position the number on the screen
                    font = pygame.font.Font(None, 30)
                    text_surface = font.render(str(number), True, BLACK)
                    text_rect = text_surface.get_rect(center=(x * cell_size + cell_size / 2, y * cell_size + cell_size / 2))
                    screen.blit(text_surface, text_rect)

        pygame.display.update()

    maze_clone = maze.copy()
    maze_width = len(maze_clone[0])
    maze_height = len(maze_clone)
    cell_size = 30

    if visualize == "False" or visualize == "false" or visualize == None:
        for unfinish_path in expanded_nodes:
            for node in unfinish_path:
                x, y = node
                if node == start or node == goal or (maze_clone[y][x] > '0' and maze_clone[y][x] <= '9'):
                    continue
                maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]
        if path is not None:
            for node in path:
                x, y = node
                if node == start or node == goal or (maze_clone[y][x] > '0' and maze_clone[y][x] <= '9'):
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
                if node == start or node == goal or (maze_clone[y][x] > '0' and maze_clone[y][x] <= '9'):
                    continue
                maze_clone[y] = maze_clone[y][:x] + '▒' + maze_clone[y][x + 1:]
            draw_maze(screen, maze_clone)
            images_list.append(np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface()), 1)))

            # pygame.time.delay(5)  # Delay for 5 milliseconds

        if path is not None:
            for node in path:
                x, y = node
                if node == start or node == goal or (maze_clone[y][x] > '0' and maze_clone[y][x] <= '9'):
                    continue
                maze_clone[y] = maze_clone[y][:x] + '█' + maze_clone[y][x + 1:]
                draw_maze(screen, maze_clone)

        for i in range(30):
            images_list.append(np.flipud(np.rot90(pygame.surfarray.array3d(pygame.display.get_surface()), 1)))

        # Lưu video
        imageio.mimsave(output_path + ".mp4", images_list, fps=30, quality=5, codec="libx264", pixelformat="yuv420p")
        
        pygame.quit()

    return maze_clone


def find_path(algo, maze, output_path, start, goal, mapping_teleport, heuristic=None, visualize=None):
    path, cost, expanded_nodes, runtime = algo(maze, start, goal, mapping_teleport, heuristic)

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
                        default='ucs_teleport',
                        choices=['ucs_teleport', 'a_star_teleport'], help='Search algorithm to use')
    parser.add_argument('--heuristic', type=str, 
                        default='',
                        choices=['','1', '2'], help='Heuristic for GBFS and A*')
    parser.add_argument('--visualize', type=str, 
                        default='False',
                        choices=['True', 'False'], help='Visualize the search process in PyGame')

    args = parser.parse_args()

    # input\level_1\input1.txt
    input_path = args.maze
    algorithm = args.algorithm
    heuristic = args.heuristic

    # custom output heuristic path extention
    if heuristic != "":
        output_path = os.path.join(input_path.replace("input\\", "output\\").split(".")[0], algorithm + "_heuristic_" + str(heuristic))
    else:
        output_path = os.path.join(input_path.replace("input\\", "output\\").split(".")[0], algorithm)
    output_path = os.path.join(output_path)

    # Create output path
    if not os.path.exists(output_path):
        os.makedirs(output_path, exist_ok=True)
    output_path = os.path.join(output_path, algorithm)

    # Load maze, find start and goal, and call the appropriate search algorithm
    maze, mapping_teleport = load_maze(args.maze)
    start, goal = find_start_goal(maze)

    if args.algorithm == 'ucs_teleport':
        cost, expanded_nodes_counter, runtime = find_path(ucs_teleport, maze, output_path, start, goal, mapping_teleport, visualize=args.visualize)

    with open(output_path + ".txt", "w") as file:
        if (cost is not None):
            file.write(str(cost))
        else:
            file.write("NO")

    #### Example of how to call the search algorithms ####
    # > python source\pygame_halfBonus_maze.py --maze input\advance\input1.txt --visualize True
