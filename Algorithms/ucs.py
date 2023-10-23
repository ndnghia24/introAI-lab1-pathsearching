import heapq


def ucs(maze, start_position, end_position):
    rows = len(maze)
    cols = len(maze[0])
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]

    visited = set()
    priority_queue = [(0, start_position)]  # Sửa đổi ở đây: Dùng 0 làm chi phí ban đầu
    came_from = {}  # Sửa đổi ở đây: Lưu lại thông tin đường đi

    while priority_queue:
        current_cost, current_position = heapq.heappop(priority_queue)

        if current_position == end_position:
            path = reconstruct_path(start_position, end_position, came_from)
            return path

        if current_position in visited:
            continue

        visited.add(current_position)

        for dx, dy in directions:
            nx, ny = current_position[0] + dx, current_position[1] + dy
            neighbor_position = (nx, ny)

            if (
                0 <= nx < cols
                and 0 <= ny < rows
                and maze[ny][nx] != "x"
                and neighbor_position not in visited
            ):
                new_cost = (
                    current_cost + 1
                )  # Sửa đổi ở đây: Cộng thêm 1 đơn vị cho chi phí

                if (
                    neighbor_position not in came_from
                    or new_cost < came_from[neighbor_position][0]  # Sửa đổi ở đây
                ):
                    came_from[neighbor_position] = (
                        new_cost,
                        current_position,
                    )  # Sửa đổi ở đây
                    priority = new_cost
                    heapq.heappush(priority_queue, (priority, neighbor_position))

    return None


def reconstruct_path(start, end, came_from):
    path = [end]
    current = end

    while current != start:
        current = came_from[current][1]  # Sửa đổi ở đây
        path.append(current)

    path.reverse()
    return path
