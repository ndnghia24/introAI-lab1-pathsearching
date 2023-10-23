def dfs(maze, start_position, end_position):
    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    # Tạo một ma trận để theo dõi các ô đã được ghé thăm
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    # Ngăn xếp để theo dõi các nút cần kiểm tra
    stack = [(start_position, [start_position])]

    while stack:
        (x, y), path = stack.pop()

        # Đã đến điểm kết thúc, trả về đường đi
        if (x, y) == end_position:
            return path

        # Đánh dấu ô hiện tại là đã ghé thăm
        visited[y][x] = True

        # Kiểm tra các ô láng giềng có thể di chuyển đến
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and not visited[ny][nx]
                and maze[ny][nx] != "x"
            ):
                new_path = path + [(nx, ny)]
                stack.append(((nx, ny), new_path))

    # Không tìm thấy đường đi
    return None