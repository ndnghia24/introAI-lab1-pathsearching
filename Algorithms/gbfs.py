from queue import PriorityQueue

def gbfs(maze, start, goal, heuristic):
    # Kiểm vị trí S và G trong ma trận
    if start == None or goal == None:
        print("S and G not found")
        return None, 0
    
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'

    # Hướng di chuyển trong maze
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    def heuristic(node, goal):
        return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5

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
                priority_queue.put((heuristic(next_node, goal), next_node, path + [current_node]))

    return None, None
