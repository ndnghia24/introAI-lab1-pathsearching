import sys
import heapq
import time
import math
from collections import deque

def a_star(maze, start, goal, heuristic):
    # Kiểm vị trí S và G trong ma trận
    if start is None or goal is None:
        print("S and G not found")
        return None, None, None, None

    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'

    # Hướng di chuyển trong maze
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    # 1: Hàm heuristic khoảng cách Manhattan
    def heuristic_manhattan(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    # 2: Hàm heuristic khoảng cách Euclidean
    def heuristic_euclidean(node, goal):
        return math.sqrt(pow((node[0] - goal[0]), 2) + pow((node[1] - goal[1]), 2))

    # 3: Hàm heuristic khoảng cách Chebyshev
    def heuristic_chebyshev(node, goal):
        return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))

    START_TIME = time.perf_counter()
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, (1, start, [start])))
    expanded_nodes = []

    while priority_queue:
        priority, (current_cost, current_node, path) = heapq.heappop(priority_queue)

        if current_node == goal:
            return path, len(path)-1, expanded_nodes, time.perf_counter() - START_TIME

        if current_node in visited:
            continue

        visited.add(current_node)

        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                next_node = (new_x, new_y)
                new_cost = current_cost + math.sqrt(dx * dx + dy * dy)

                if heuristic == "1":
                    priority = new_cost + heuristic_manhattan(next_node, goal)
                elif heuristic == "2":
                    priority = new_cost + heuristic_euclidean(next_node, goal)
                elif heuristic == "3":
                    priority = new_cost + heuristic_chebyshev(next_node, goal)
                else:
                    print("Heuristic not found")
                    return None, None, None, None

                # double heuristic
                # priority += heuristic_manhattan(next_node, goal)

                heapq.heappush(priority_queue, (priority, (new_cost, next_node, path + [next_node])))
                expanded_nodes.append(path + [next_node])

    return None, None, None, None


def construct_bonus_maze(bonus_point,maze):
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'
    
    q = deque()
    q.append(bonus_point)
    distance = {}
    distance[bonus_point] = 0

    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    while not len(q) == 0:
        current_node = q.popleft()
        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and (new_x,new_y) not in distance:
                distance[(new_x,new_y)] = distance[current_node] + 1
                q.append((new_x,new_y))
    return distance


def bonus(maze,start,goal,mapping_bonus, heuristic=None):
    bonus_point = list(mapping_bonus.keys())
    dict_maze = {} 

    # xay dung ban do khoang cach 
    # dong thoi loai bo nhung diem ma duong di ngan nhat tu diem do den goal lon hon gia tri cua diem thuong do
    for i in range(len(bonus_point)):
        if (i > len(bonus_point) - 1): break
        dict_maze[bonus_point[i]] = construct_bonus_maze(bonus_point[i],maze)

    dict_maze[start] = construct_bonus_maze(start,maze)

    current_node = start

    path = []
    cost = 0
    expandNode = []

    while current_node != goal:
        point = None
        min_heuristic = sys.maxsize
        for items in bonus_point:
            heuristic = dict_maze[items][current_node] + mapping_bonus[items] + dict_maze[items][goal]
            if heuristic < min_heuristic:
                min_heuristic = heuristic
                point = items
    
        if min_heuristic == sys.maxsize:
            # khong co diem thuong nao co the loi duong khi di den goal 
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,goal,heuristic="1") # heuristic_manhattan
            path = path + t_path
            cost = cost + t_cost
            expandNode = expandNode + t_expandedNode
            current_node = goal
        elif min_heuristic > dict_maze[current_node][goal]:
            # diem thuong khong loi duong khi den goal
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,goal,heuristic="1") # heuristic_manhattan
            path = path + t_path
            cost = cost + t_cost
            expandNode = expandNode + t_expandedNode
            current_node = goal
        else:
            # diem thuong co loi duong khi den goal
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,point,heuristic="1") # heuristic_manhattan
            path = path + t_path
            cost = cost + t_cost + mapping_bonus[point]
            expandNode = expandNode + t_expandedNode
            current_node = point
            bonus_point.remove(point)

    return path,cost,expandNode,0