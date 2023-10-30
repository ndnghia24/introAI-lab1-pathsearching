import heapq
import math

def a_star_modified(maze,start,goal,map_bonus) -> (list, int):
    # the heuristic use for this algorithm is the manhattan distance
    
    # Kiểm vị trí S và G trong ma trận
    if start is None or goal is None:
        print("S and G not found")
        return None, None, None, None

    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'

    # Hướng di chuyển trong maze
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    # TO DO: Set the time for the algorithm
    visited = set()
    priority_queue = []
    heapq.heappush(priority_queue, (0, (1, start, [start])))
    expanded_nodes = []

    while priority_queue:
        priority, (current_cost, current_node, path) = heapq.heappop(priority_queue)

        if current_node == goal:
            return path, current_cost

        if current_node in visited:
            continue

        visited.add(current_node)

        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                if (new_x,new_y) in map_bonus:
                    current_cost += map_bonus[(new_x,new_y)] - 1
                
                next_node = (new_x, new_y)
                new_cost = current_cost + math.sqrt(dx * dx + dy * dy)

                priority = new_cost + heuristic(next_node)

                heapq.heappush(priority_queue, (priority, (new_cost, next_node, path + [next_node])))
                expanded_nodes.append(path + [next_node])

    return None, None

