import pygame
from maze import SearchSpace
from algos import DFS, BFS, UCS, AStar, GBFS
from const import GREY
import argparse
import os


def draw_button(sc, text, x, y, w, h):
    pygame.draw.rect(sc, (0, 255, 0), (x, y, w, h))
    font = pygame.font.SysFont(None, 36)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect(center=(x + w // 2, y + h // 2))
    sc.blit(text_surf, text_rect)


def main():
    your_name = "your name goes here"
    pygame.init()
    pygame.display.set_caption(f"{your_name} - Search Algorithms")
    sc = pygame.display.set_mode((1280, 768))
    clock = pygame.time.Clock()

    algo = None
    while algo is None:
        sc.fill(pygame.color.Color(GREY))

        draw_button(sc, "DFS", 50, 100, 100, 50)
        draw_button(sc, "BFS", 200, 100, 100, 50)
        draw_button(sc, "UCS", 350, 100, 100, 50)
        draw_button(sc, "AStar", 500, 100, 100, 50)
        draw_button(sc, "GBFS", 650, 100, 100, 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 200 and 100 <= y <= 150:
                    algo = "DFS"
                elif 250 <= x <= 350 and 100 <= y <= 150:
                    algo = "BFS"
                elif 400 <= x <= 500 and 100 <= y <= 150:
                    algo = "UCS"
                elif 550 <= x <= 650 and 100 <= y <= 150:
                    algo = "AStar"
                elif 700 <= x <= 800 and 100 <= y <= 150:
                    algo = 'GBFS'

    sc.fill(pygame.color.Color(GREY))

    maze_path = str(os.path.dirname(os.path.abspath(__file__))) + "\MapTest\MapNotPrize\input1.txt"
    maze_data = []

    with open(maze_path, "r") as file:
        n = int(file.readline())

        for i in range(n):
            buff = file.readline()
            coordinates = buff.split(" ")
            
            x = int(coordinates[0])
            y = int(coordinates[1])
            val = int(coordinates[2])

        maze_data = [line.rstrip() for line in file.readlines()]

    g = SearchSpace(maze_data)
    g.draw(sc)

    if algo == "DFS":
        DFS(g, sc)
    elif algo == "BFS":
        BFS(g, sc)
    elif algo == "UCS":
        UCS(g, sc)
    elif algo == "AStar":
        AStar(g, sc)
    elif algo == "GBFS":
        GBFS(g, sc)
    else:
        raise NotImplementedError("Not implemented")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == "__main__":
    main()
