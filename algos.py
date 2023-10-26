import heapq
import pygame
from const import *
from maze import SearchSpace
import math

def DFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement DFS algorithm')

    stack = [g.start]
    closed_set = set()
    father = [-1] * g.get_length()

    while stack:
        current = stack.pop()
        current.set_color(YELLOW, sc)
        if g.is_goal(current):
            path = []
            path_node = current
            while path_node.id != g.start.id:
                path.append(path_node)
                path_node = g.grid_cells[father[path_node.id]]
            path.append(g.start)

            for i in range(1, len(path)):
                pygame.draw.line(sc, WHITE, path[i-1].get_center(), path[i].get_center(), 2)

            g.start.set_color(ORANGE, sc)
            g.goal.set_color(PURPLE, sc)
            pygame.display.flip()
            print('Path found!')
            return

        closed_set.add(current.id)
        current.set_color(BLUE, sc)

        for neighbor in g.get_neighbors(current):

            if neighbor.id not in closed_set:
                if father[neighbor.id] == -1: 
                    father[neighbor.id] = current.id
                    stack.append(neighbor)
                    neighbor.set_color(RED, sc)

        current.set_color(BLUE, sc)
    print('No path found!')

def BFS(g: SearchSpace, sc: pygame.Surface):
    print('Implement BFS algorithm')

    queue = [g.start]
    closed_set = set()
    father = [-1] * g.get_length()

    while queue:
        current = queue.pop(0)
        current.set_color(YELLOW,sc)
        if g.is_goal(current):
            path_nodes = [current]

            while path_nodes[-1].id != g.start.id:
                path_nodes.append(g.grid_cells[father[path_nodes[-1].id]])

            for i in range(len(path_nodes) - 1):
                pygame.draw.line(sc, WHITE, (path_nodes[i].rect.centerx, path_nodes[i].rect.centery), 
                                 (path_nodes[i + 1].rect.centerx, path_nodes[i + 1].rect.centery), 2)
            
            g.start.set_color(ORANGE, sc)
            g.goal.set_color(PURPLE, sc)
            print('Path found!')
            return

        closed_set.add(current.id)
        current.set_color(BLUE, sc)

        for neighbor in g.get_neighbors(current):
            if neighbor.id not in closed_set and neighbor not in queue:
                father[neighbor.id] = current.id
                queue.append(neighbor)
                neighbor.set_color(RED, sc)

    print('No path found!')

def UCS(g: SearchSpace, sc: pygame.Surface):
    print('Implement UCS algorithm')
    
    open_set = [(0, g.start.id)]
    
    closed_set = set()
    father = [-1]*g.get_length()
    cost = [float('inf')]*g.get_length()
    cost[g.start.id] = 0

    while open_set:
        current_cost, current_node_id = heapq.heappop(open_set)
        current_node = g.grid_cells[current_node_id]
        current_node.set_color(YELLOW,sc)

        if g.is_goal(current_node):
            path_node = current_node
            while path_node.id != g.start.id:
                pygame.draw.line(sc, WHITE, g.grid_cells[father[path_node.id]].rect.center, path_node.rect.center, 2)
                path_node = g.grid_cells[father[path_node.id]]
            g.start.set_color(ORANGE, sc)
            g.goal.set_color(PURPLE, sc)
            print('Path found!')
            return

        closed_set.add(current_node.id)
        current_node.set_color(BLUE, sc)

        for neighbor in g.get_neighbors(current_node):
            if neighbor.id not in closed_set:
                tentative_cost = current_cost + 1
                if tentative_cost < cost[neighbor.id]:
                    cost[neighbor.id] = tentative_cost
                    father[neighbor.id] = current_node.id
                    neighbor.set_color(RED, sc)
                    heapq.heappush(open_set, (tentative_cost, neighbor.id))

    print('No path found!')


def AStar(g: SearchSpace, sc: pygame.Surface):
    print('Implementing AStar algorithm')

        #heuristic function
    def manhattan_distance(node1, node2):
        x1, y1 = node1.id % g.cols, node1.id // g.cols
        x2, y2 = node2.id % g.cols, node2.id // g.cols
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(pos1, pos2):
        (x1, y1), (x2, y2) = pos1, pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    open_set = []
    heapq.heappush(open_set, (0, g.start.id))

    closed_set = set()
    father = [-1] * g.get_length()
    g_cost = [float('inf')] * g.get_length()
    g_cost[g.start.id] = 0

    while open_set:
        current_f, current_id = heapq.heappop(open_set)
        current_node = g.grid_cells[current_id]
        current_node.set_color(YELLOW,sc)

        if current_id in closed_set:
            continue

        if g.is_goal(current_node):
            path = []
            while current_id != g.start.id:
                path.append(current_id)
                current_id = father[current_id]
            path.append(g.start.id)
            path.reverse()

            for idx in range(1, len(path)):
                start_node = g.grid_cells[path[idx - 1]]
                end_node = g.grid_cells[path[idx]]
                pygame.draw.line(sc, WHITE, start_node.get_center(), end_node.get_center(), 2)
            g.start.set_color(ORANGE, sc)
            g.goal.set_color(PURPLE, sc)
            pygame.display.update()
            return

        closed_set.add(current_id)
        current_node.set_color(BLUE, sc)
        pygame.display.update()

        for neighbor in g.get_neighbors(current_node):
            if neighbor.id not in closed_set:
                tentative_g = g_cost[current_id] + 1

                if tentative_g < g_cost[neighbor.id]:
                    father[neighbor.id] = current_id
                    g_cost[neighbor.id] = tentative_g
                    h = manhattan_distance(neighbor, g.goal)
                    f = tentative_g + h
                    neighbor.set_color(RED, sc)
                    pygame.display.update()
                    heapq.heappush(open_set, (f, neighbor.id))

    print('No path found!')
    return

def GBFS(g: SearchSpace, sc: pygame.Surface):
    print('Implementing GBFS algorithm')

            #heuristic function
    def manhattan_distance(node1, node2):
        x1, y1 = node1.id % g.cols, node1.id // g.cols
        x2, y2 = node2.id % g.cols, node2.id // g.cols
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(pos1, pos2):
        (x1, y1), (x2, y2) = pos1, pos2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    open_set = []
    heapq.heappush(open_set, (0, g.start.id))

    closed_set = set()
    father = [-1] * g.get_length()

    while open_set:
        current_f, current_id = heapq.heappop(open_set)
        current_node = g.grid_cells[current_id]
        current_node.set_color(YELLOW,sc)

        if current_id in closed_set:
            continue

        if g.is_goal(current_node):
            path = []
            while current_id != g.start.id:
                path.append(current_id)
                current_id = father[current_id]
            path.append(g.start.id)
            path.reverse()

            for idx in range(1, len(path)):
                start_node = g.grid_cells[path[idx - 1]]
                end_node = g.grid_cells[path[idx]]
                pygame.draw.line(sc, WHITE, start_node.get_center(), end_node.get_center(), 2)
            g.start.set_color(ORANGE, sc)
            g.goal.set_color(PURPLE, sc)
            pygame.display.update()
            return

        closed_set.add(current_id)
        current_node.set_color(BLUE, sc)
        pygame.display.update()

        for neighbor in g.get_neighbors(current_node):
            if neighbor.id not in closed_set:
                father[neighbor.id] = current_id
                h = manhattan_distance(neighbor, g.goal)
                neighbor.set_color(RED, sc)
                pygame.display.update()
                heapq.heappush(open_set, (h, neighbor.id))

    print('No path found!')
    return
