import math
import time
import heapq

def ucs(maze, start, goal, heuristic=None):
    print("UCS Function")
    
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'
    
    # Hướng di chuyển trong maze
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    START_TIME = time.perf_counter()
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, (start, [start])))
    expanded_nodes = []

    while priority_queue:
        current_cost, (current_node, path) = heapq.heappop(priority_queue)

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
                heapq.heappush(priority_queue, (new_cost, (next_node, path + [next_node])))
                expanded_nodes.append(path + [next_node])

    return None, None, None, None
