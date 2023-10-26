import pygame
from const import *
import random

# you can change the random seed but when you submit your work, it should be run on my random seed!
random.seed(2345)

class Node:    
    def __init__(self, x, y, a, id, is_brick=False) -> None:
        self.rect = pygame.Rect(x, y, a, a)
        self.is_brick = is_brick
        self.color = BLACK if self.is_brick else WHITE
        self.id = id

    def draw(self, sc:pygame.Surface) -> None:
        pygame.draw.rect(sc, self.color, self.rect)

    def _set_color(self, color):
        self.color = color

    def set_color(self, color, sc:pygame.Surface):
        self.color = color
        self.draw(sc)

        # change the speed here
        pygame.time.delay(5)
        pygame.display.update()
    
    def get_center(self):
        return self.rect.centerx, self.rect.centery

class SearchSpace:
    def __init__(self, maze_data) -> None:
        self.grid_cells:list[Node] = []
        print(maze_data)
        self.rows = maze_data.__len__()
        self.cols = maze_data[0].__len__()
        for i in range(self.rows):
            for j in range(self.cols):
                # 
                is_brick = True if maze_data[i][j] == "x" else False
                self.grid_cells.append(Node(j*20, i*20, 20, i*self.cols+j, is_brick))
                if (maze_data[i][j] == "S"):
                    self.start:Node = self.grid_cells[i*self.cols+j]
                if (maze_data[i][j] == "G"):
                    self.goal:Node = self.grid_cells[i*self.cols+j]

        self.start._set_color(ORANGE)
        self.goal._set_color(PURPLE)

    def draw(self, sc:pygame.Surface):
        for node in self.grid_cells:
            node.draw(sc)
        pygame.display.flip()

    def get_length(self):
        return len(self.grid_cells)

    def is_goal(self, node:Node):
        return node.id == self.goal.id

    def get_neighbors(self, node: Node) -> list[Node]:
        x, y = node.id % self.cols, node.id // self.cols

        # define the directions of agent
        up    = (y-1)*self.cols + x if y-1 >= 0 else None
        down  = (y+1)*self.cols + x if y+1 < self.rows else None
        left  = y*self.cols + (x-1) if x-1 >= 0 else None
        right = y*self.cols + (x+1) if x+1 < self.cols else None

        directions = [up, down, left, right]
        # directions = [up, down, left, right]
        neighbors = []
        for dir_ in directions:
            if dir_ is not None and not self.grid_cells[dir_].is_brick:
                neighbors.append(self.grid_cells[dir_])

        return neighbors