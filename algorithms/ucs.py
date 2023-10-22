from queue import PriorityQueue

# Hàm thực hiện thuật toán UCS
def ucs(maze, mapping_bonus, start, goal):
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= x < len(maze)) and (0 <= y < len(maze[0])) and maze[x][y] != 'x'
    
    # Hướng di chuyển trong maze
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Hàm cost trả về chi phí di chuyển từ ô hiện tại đến ô kế tiếp
    def cost(current, next):
        return 1

    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((0, start, []))

    while not priority_queue.empty():
        current_cost, current_node, path = priority_queue.get()

        if current_node == goal:
            return current_cost, path

        if current_node in visited:
            continue

        visited.add(current_node)

        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y):
                next_node = (new_x, new_y)
                new_cost = current_cost + cost(current_node, next_node)
                priority_queue.put((new_cost, next_node, path + [current_node]))

    return None, None
