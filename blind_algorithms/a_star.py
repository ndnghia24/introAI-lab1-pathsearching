import math
import time
import heapq

def a_star(maze, start, goal, heuristic):
    print("A* Function")

    # Kiểm vị trí S và G trong ma trận
    if start is None or goal is None:
        print("S and G not found")
        return None, 0

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
            return path, len(path), expanded_nodes, time.perf_counter() - START_TIME

        if current_node in visited:
            continue

        visited.add(current_node)

        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                next_node = (new_x, new_y)
                new_cost = current_cost + math.sqrt(dx * dx + dy * dy)

                if heuristic == "heuristic_manhattan":
                    priority = new_cost + heuristic_manhattan(next_node, goal)
                elif heuristic == "heuristic_euclidean":
                    priority = new_cost + heuristic_euclidean(next_node, goal)
                elif heuristic == "heuristic_chebyshev":
                    priority = new_cost + heuristic_chebyshev(next_node, goal)
                else:
                    print("Heuristic not found")
                    return None, None, None

                # double heuristic
                # priority += heuristic_manhattan(next_node, goal)

                heapq.heappush(priority_queue, (priority, (new_cost, next_node, path + [next_node])))
                expanded_nodes.append(path + [next_node])

    return None, None, None, None
