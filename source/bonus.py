from pygame_maze import *
from blind_algorithms.a_star import a_star_modified
import sys
import heapq

maze,mapping_bonus = load_maze("D:\Study\introAI-lab1-pathsearching\input\level_2\input1.txt")
start,goal = find_start_goal(maze)

def dijkstra(matrix, start):
    n = len(matrix)  # Số lượng đỉnh
    distances = [float('infinity')] * n  # Khởi tạo mảng khoảng cách
    distances[start] = 0
    visited = [False] * n
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Đảm bảo rằng không xử lý một đỉnh nhiều hơn một lần
        if visited[current_vertex]:
            continue
        visited[current_vertex] = True

        for neighbor in range(n):
            # Kiểm tra xem có cạnh nối từ current_vertex tới neighbor hay không
            if matrix[current_vertex][neighbor] != 0 and not visited[neighbor]:
                distance = current_distance + matrix[current_vertex][neighbor]
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances

def chuan_hoa_ma_tran(matrix):
    min = sys.maxsize
    for line in matrix:
        for items in line:
            if items != 0 and items < min:
                min = items

    if min < 0:
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    matrix[i][j] -= min


nodes = tuple([start]) + tuple(mapping_bonus.keys()) + tuple([goal])

print(start)
print(goal)

print(maze)
print(mapping_bonus)

print(nodes)

matrix = []

for node1 in nodes:
    line = []
    for node2 in nodes:
        if node1 == node2:
            line.append(0)
        else:
            path, cost = a_star_modified(maze, node1, node2, mapping_bonus)
            if cost == None:
                line.append(0)
            else:
                line.append(cost)
    matrix.append(line)

for line in matrix:
    print(line)

chuan_hoa_ma_tran(matrix)
print("Chuan hoa")

for line in matrix:
    print(line)



