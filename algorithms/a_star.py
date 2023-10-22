from queue import PriorityQueue

def a_star(maze, start, goal, heuristic):
    # Kiểm vị trí S và G trong ma trận
    if start == None or goal == None:
        print("S and G not found")
        return None, 0
    
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and maze[x][y] != 'x'
    
    # Hướng di chuyển trong maze
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # 1: Hàm heuristic khoảng cách Manhattan
    def heuristic_manhattan(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    
    # 2: Hàm heuristic xét đường chim bay
    def heuristic_euclidean(node, goal):
        return pow((node[0] - goal[0]), 2) + pow((node[1] - goal[1]), 2)
    
    # 3: Hàm heuristic khoảng cách Chebyshev
    def heuristic_chebyshev(node, goal):
        return max(abs(node[0] - goal[0]), abs(node[1] - goal[1]))

    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, []))

    while not priority_queue.empty():
        current_cost, current_node, path = priority_queue.get()

        if current_node == goal:
            return len(path), path

        if current_node in visited:
            continue

        visited.add(current_node)

        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                next_node = (new_x, new_y)
                new_cost = current_cost + 1
                match  heuristic:
                    case 1:
                        priority_queue.put((new_cost + heuristic_manhattan(next_node, goal), next_node, path + [current_node]))
                    case 2:
                        priority_queue.put((new_cost + heuristic_euclidean(next_node, goal), next_node, path + [current_node]))
                    case 3:
                        priority_queue.put((new_cost + heuristic_chebyshev(next_node, goal), next_node, path + [current_node]))

    return None, None
