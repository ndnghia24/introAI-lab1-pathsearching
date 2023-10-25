import heapq
import math


def euclidean_distance(pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def manhattan_distance(pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    return abs(x1 - x2) + abs(y1 - y2)


def gbfs(maze, start_position, end_position, heuristic):
    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Sử dụng heap để lưu trữ các nút với giá trị heuristic và đường đi
    heap = [(heuristic(start_position, end_position), [start_position])]

    while heap:
        h, path = heapq.heappop(heap)
        x, y = path[-1]

        # Kiểm tra nếu đã đến điểm đích
        if (x, y) == end_position:
            return path  # Trả về đường đi đã tìm thấy

        visited[y][x] = True

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and not visited[ny][nx]
                and maze[ny][nx] != "x"
            ):
                new_path = path + [(nx, ny)]
                heapq.heappush(heap, (heuristic((nx, ny), end_position), new_path))

    return None  # Không tìm thấy đường đi
