from pygame_maze import *
from blind_algorithms.a_star import a_star_modified
import sys
import heapq
from collections import deque

maze,mapping_bonus = load_maze("D:\Study\introAI-lab1-pathsearching\input\level_2\input3.txt")
start,goal = find_start_goal(maze)

def construct_bonus_maze(bonus_point,maze):
    # Hàm để kiểm tra đường đi hợp lệ
    def is_valid(x, y):
        return (0 <= y < len(maze)) and (0 <= x < len(maze[0])) and maze[y][x] != 'x'
    
    q = deque()
    q.append(bonus_point)
    distance = {}
    distance[bonus_point] = 0

    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    while not len(q) == 0:
        current_node = q.popleft()
        x, y = current_node
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y) and (new_x,new_y) not in distance:
                distance[(new_x,new_y)] = distance[current_node] + 1
                q.append((new_x,new_y))
    return distance

def bonus(maze,start,goal,mapping_bonus):
    bonus_point = list(mapping_bonus.keys())
    dict_maze = {}

    print(bonus_point)  

    # xay dung ban do khoang cach 
    # dong thoi loai bo nhung diem ma duong di ngan nhat tu diem do den goal lon hon gia tri cua diem thuong do
    for i in range(len(bonus_point)):
        if (i > len(bonus_point) - 1): break
        dict_maze[bonus_point[i]] = construct_bonus_maze(bonus_point[i],maze)

    for items in bonus_point:
        if (dict_maze[items][goal] +  mapping_bonus[items] > 0):
            bonus_point.remove(items)

    current_node = start
    print(bonus_point)
    print(dict_maze.keys())

    path = []
    cost = 0
    expandNode = []

    while current_node != goal:
        point = None
        min_heuristic = sys.maxsize
        for items in bonus_point:
            heuristic = dict_maze[items][current_node] + mapping_bonus[items] + dict_maze[items][goal]
            print(heuristic)
            print(mapping_bonus[items])
            if heuristic < min_heuristic:
                min_heuristic = heuristic
                point = items
        
        print(min_heuristic)
        print(point)

        if min_heuristic == sys.maxsize:
            # khong co diem thuong nao co the loi duong khi di den goal 
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,goal,heuristic="heuristic_manhattan")
            path = path + t_path
            cost = cost + t_cost
            expandNode = expandNode + t_expandedNode
            current_node = goal
        elif min_heuristic > 0:
            # diem thuong khong loi duong khi den goal
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,goal,heuristic="heuristic_manhattan")
            path = path + t_path
            cost = cost + t_cost
            expandNode = expandNode + t_expandedNode
            current_node = goal
        else:
            # diem thuong co loi duong khi den goal
            t_path,t_cost,t_expandedNode,temp = a_star(maze,current_node,point,heuristic="heuristic_manhattan")
            path = path + t_path
            cost = cost + t_cost + mapping_bonus[point]
            expandNode = expandNode + t_expandedNode
            current_node = point
            bonus_point.remove(point)
            print(bonus_point)

    return path,cost,expandNode

path,cost,expandNode = bonus(maze,start,goal,mapping_bonus=mapping_bonus)
print_maze_result(maze,"D:\Study\introAI-lab1-pathsearching\output\level_2\output3.txt",path,cost,expandNode,visualize="True")

print(cost)

# print(mapping_bonus)

# for key in mapping_bonus:
#     dic = construct_bonus_maze(key,maze)
#     break

# for i in range(len(maze)):
#     for j in range(len(maze[i])):
#         if (j,i) in dic:
#             print(dic[(j,i)],end=" ")
#         else:
#             print("x",end=" ")
#     print()

