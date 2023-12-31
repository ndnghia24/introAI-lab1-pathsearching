import time

def dfs(maze, start, goal, heuristic=None):
    print("DFS Function")

    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'
    
    # Hướng di chuyển trong maze
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    START_TIME = time.perf_counter()
    visited = set()
    stack = [(start, [start])]
    expanded_nodes = []

    while stack:
        current_node, path = stack.pop()
        
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
                stack.append((next_node, path + [next_node]))
                expanded_nodes.append(path + [next_node])

    return None, None, None, None
