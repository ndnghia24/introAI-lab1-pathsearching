import heapq
import math

# Hàm heuristic - khoảng cách Euclidean
def euclidean_distance(pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Hàm heuristic - khoảng cách Manhattan
def manhattan_distance(pos1, pos2):
    (x1, y1), (x2, y2) = pos1, pos2
    return abs(x2 - x1) + abs(y2 - y1)

# Thuật toán A*
def astar(maze, start_position, end_position, heuristic):
    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    # Sử dụng heap để lưu trữ các nút với chi phí thực tế và đường đi
    heap = [(0 + heuristic(start_position, end_position), 0, start_position, [])]

    while heap:
        f, g, (x, y), path = heapq.heappop(heap)

        if (x, y) == end_position:
            return path + [(x, y)]  # Trả về đường đi đã tìm thấy

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] != "x":
                new_g = g + 1
                new_path = path + [(x, y)]
                heapq.heappush(heap, (new_g + heuristic((nx, ny), end_position), new_g, (nx, ny), new_path))

    return None  # Không tìm thấy đường đi