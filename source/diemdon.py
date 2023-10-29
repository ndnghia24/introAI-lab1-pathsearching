from pygame_maze import *
from itertools import permutations
import sys
from blind_algorithms.a_star import a_star

maze,mapping_bonus = load_maze("input\level_3\input3.txt")

start,goal = find_start_goal(maze)


diem_don = list(mapping_bonus.keys())

def find_path_with_diem_don(maze,start,goal,diem_don):
    nodes = tuple([start]) + tuple(mapping_bonus.keys()) + tuple([goal]) 
    matrix = []

    for i in nodes:
        line = []
        for j in nodes:
            if i == j:
                line.append(([],0,[]))
            else:
                path,cs,expand,n = a_star(maze,i,j,heuristic="heuristic_manhattan")
                if (path == None): return None,None,None
                line.append((path,cs,expand))
        matrix.append(line)
    start = 0
    goal = len(nodes) - 1
    diem_don = list(range(0,len(diem_don)-1))
    for line in matrix:
        print(line)
    if(len(diem_don) <= 10):
        return find_path_with_diem_don_less_than_10(maze,start,goal,diem_don,matrix)
    else:
        return find_path_with_diem_don_greater_than_10(maze,start,goal,diem_don,matrix)
    
def find_path_with_diem_don_less_than_10 (maze,start,goal,diem_don,matrix):
    if len(diem_don) == 0:
        return matrix[start][goal][0],matrix[start][goal][1],matrix[start][goal][2]
    else: 
        result = None
        cost = sys.maxsize
        perm = permutations(diem_don)
        expandNode = []
        for i in list(perm):
            expandnode = []
            path = matrix[start][i[0]][0]
            cs = matrix[start][i[0]][1]
            expandnode = expandnode + matrix[start][i[0]][2]
            for j in range(len(i)-1):
                path = path + matrix[i[j]][i[j+1]][0]
                cs = cs + matrix[i[j]][i[j+1]][1]
                expandnode = expandnode + matrix[i[j]][i[j+1]][2]
            path = path + matrix[i[len(i)-1]][goal][0]
            cs = cs + matrix[i[len(i)-1]][goal][1]
            expandnode = expandnode + matrix[i[len(i)-1]][goal][2]
            if cs < cost:
                cost = cs
                result = path
                expandNode = expandnode

        return result,cost,expandnode

def find_path_with_diem_don_greater_than_10 (maze,start,goal,diem_don,matrix):
    neighbor = []
    first_ten = permutations(diem_don[0:10])

    for i in list(first_ten):
        neighbor.append(list(i) + diem_don[10:])

    print("here 1")

    cost = sys.maxsize
    result = None
    thu_tu = None
    expandNode = []

    for i in neighbor:
        expandnode = []
        path = matrix[start][i[0]][0]
        cs = matrix[start][i[0]][1]
        expandnode = expandnode + matrix[start][i[0]][2]
        if path != None:
            for j in range(len(i)-1):
                path = path + matrix[i[j]][i[j+1]][0]
                cs = cs + matrix[i[j]][i[j+1]][1]
                expandnode = expandnode + matrix[i[j]][i[j+1]][2]
            path = path + matrix[i[len(i)-1]][goal][0]
            cs = cs + matrix[i[len(i)-1]][goal][1]
            expandnode = expandnode + matrix[i[len(i)-1]][goal][2]
            if len(path) < cost:
                cost = len(path)
                result = path
                expandNode = expandnode
                thu_tu = i

    if result == None: return None,None,None

    check = True
    
    while(1):
        neightbor = []
        first_ten = permutations(thu_tu[0:10])

        for i in list(first_ten):
            neightbor.append(i + thu_tu[10:])

        for i in neighbor:
            expandnode = []
            path = matrix[start][i[0]][0]
            cs = matrix[start][i[0]][1]
            expandnode = expandnode + matrix[start][i[0]][2]
            for j in range(len(i) - 1):
                path = path + matrix[i[j]][i[j+1]][0]
                cs = cs + matrix[i[j]][i[j+1]][1]
                expandnode = expandnode + matrix[i[j]][i[j+1]][2]
            path = path + matrix[i[len(i)-1]][goal][0]
            cs = cs + matrix[i[len(i)-1]][goal][1]
            expandnode = expandnode + matrix[i[len(i)-1]][goal][2]
            if len(path) < cost:
                check = False
                cost = len(path)
                result = path
                thu_tu = i
                expandNode = expandnode

        if check: break

    return result,cost,expandNode

path,cost,expandNode = find_path_with_diem_don(maze,start,goal,diem_don)
print_maze_result(maze,"D:\Study\introAI-lab1-pathsearching\output\level_3\output3.txt",path,cost,expandNode,visualize="True")
        

