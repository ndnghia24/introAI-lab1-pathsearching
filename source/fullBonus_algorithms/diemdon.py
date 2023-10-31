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


def construct_bonus_maze(diem_don,maze):
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'
    
    q = deque()
    q.append(diem_don)
    distance = {}
    distance[diem_don] = 0

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


def find_path_with_diem_don(maze,start,goal,diemdon, heuristic=None):
    diem_don = list(diemdon.keys())
    dict_maze = {} 

    # xay dung ban do khoang cach 
    # dong thoi loai bo nhung diem ma duong di ngan nhat tu diem do den goal lon hon gia tri cua diem thuong do
    for i in range(len(diem_don)):
        if (i > len(diem_don) - 1): break
        dict_maze[diem_don[i]] = construct_bonus_maze(diem_don[i],maze)

    dict_maze[start] = construct_bonus_maze(start,maze)

    current_node = start

    path = []
    cost = 0
    expandNode = []

    while len(diem_don) > 0:
        point = None
        min_heuristic = sys.maxsize

        for items in diem_don:
            # khoang cach tu diem don den diem hien tai
            if (items, current_node) in dict_maze:
                heuristic = dict_maze[items][current_node]
            else:
                return None, None, None, None
            
            if heuristic < min_heuristic:
                min_heuristic = heuristic
                point = items
        
        if min_heuristic == sys.maxsize:
            return None, None, None, None
        else:
            t_path, t_cost, t_expandNode, t_time = a_star(maze,current_node,point,heuristic="1")
            path = path + t_path
            # di vao diem don khong tinh chi phi nen ta - 1
            cost = cost + t_cost - 1
            expandNode = expandNode + t_expandNode
            current_node = point
            diem_don.remove(point)

    t_path, t_cost, t_expandNode, t_time = a_star(maze,current_node,goal,heuristic="1")
    path = path + t_path
    cost = cost + t_cost
    expandNode = expandNode + t_expandNode

    return path,cost,expandNode,0