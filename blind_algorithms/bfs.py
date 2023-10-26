from collections import deque

def bfs(maze, start_position, end_position, heuristic=None):
    print("BFS Function")

    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    visited = set()
    queue = deque()
    queue.append((start_position, [start_position]))
    visited.add(start_position)
    expanded_nodes = []

    while queue:
        current_position, path = queue.popleft()

        x, y = current_position

        if current_position == end_position:
            return path, len(path), expanded_nodes

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and maze[ny][nx] != "x"
                and (nx, ny) not in visited
            ):
                visited.add((nx, ny))
                new_path = path + [(nx, ny)]
                queue.append(((nx, ny), new_path))
                expanded_nodes.append(new_path)

    return None, None, None