from pygame_maze import *
from itertools import permutations
import sys
from noBonus_algorithms.a_star import a_star
import random

def find_path_with_diem_don(maze,start,goal,mapping_bonus, heuristic=None):
    diem_don = list(mapping_bonus.keys())

    nodes = tuple([start]) + tuple(mapping_bonus.keys()) + tuple([goal]) 
    matrix = []

    for i in nodes:
        line = []
        for j in nodes:
            if i == j:
                line.append(([],0,[]))
            else:
                path,cs,expand,n = a_star(maze,i,j,heuristic="1") # heuristic_manhattan
                if (path == None): return None,None,None,0
                line.append((path,cs,expand))
        matrix.append(line)
    start = 0
    goal = len(nodes) - 1
    diem_don = list(range(1,len(nodes)-1))
    # for line in matrix:
    #     print(line)
    if(len(diem_don) < 10):
        return find_path_with_diem_don_less_than_10(maze,start,goal,diem_don,matrix)
    else:
        return find_path_with_diem_don_greater_than_10(maze,start,goal,diem_don,matrix)
    
def find_path_with_diem_don_less_than_10 (maze,start,goal,diem_don,matrix):
    if len(diem_don) == 0:
        return matrix[start][goal][0],matrix[start][goal][1],matrix[start][goal][2],0
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

        return result,cost,expandnode,0

def find_path_with_diem_don_greater_than_10 (maze,start,goal,diem_don,matrix):
    # diem don chua thu tu cac diem don se duoc tham 
    # hien tai thu tu tham cua cac diem don la tang dan tu 1 
    # nen ta se goi ham random de tao ra mot thu tu ngau nhien

    # random.shuffle(diem_don)
    # khoi tao 
    result = None
    current_state = diem_don
    cost = sys.maxsize
    expanded_node = []

    init = []
    per = permutations(diem_don[:8])
    for i in list(per):
        init.append(list(i) + diem_don[8:])

    for i in range(len(init)):
        path = matrix[start][init[i][0]][0]
        cs = matrix[start][init[i][0]][1]
        expandnode = matrix[start][init[i][0]][2]
        
        for j in range(len(init[i])-1):
            path = path + matrix[init[i][j]][init[i][j+1]][0]
            cs = cs + matrix[init[i][j]][init[i][j+1]][1]
            expandnode = expandnode + matrix[init[i][j]][init[i][j+1]][2]

        path = path + matrix[init[i][len(init[i])-1]][goal][0]
        cs = cs + matrix[init[i][len(init[i])-1]][goal][1]
        expandnode = expandnode + matrix[init[i][len(init[i])-1]][goal][2]

        if len(path) < cost:
            cost = len(path)
            result = path
            current_state = init[i]
            expanded_node = expandnode

    check = True

    first_cost = cost
    
    while(1):
        neighbor = find_neighbor(current_state)

        for i in neighbor:
            check = True
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
                # print(cost)
                cost = len(path)
                result = path
                current_state = i
                expanded_node = expandnode
                # print(len(path))  

        if check: break
    return result,cost,expanded_node,0

def find_neighbor(current_state):
    res = []
    perm = permutations(current_state[:6])

    for i in list(perm):
        res.append(list(i) + current_state[6:])

    for i in range(int(len(current_state)/2)):
        res.append(reverse_sublist(current_state,i,len(current_state)-1-i))
        res.append(reverse_sublist(current_state,0,len(current_state)-1-i))
        res.append(reverse_sublist(current_state,i,len(current_state)-1))
    return res

def reverse_sublist(list,x,y):
    if x < 0 or y > len(list) - 1:
        return None
    lst = list[x:y+1]
    temp = list.copy()
    lst.reverse()
    temp[x:y+1] = lst
    return temp