import algorithms.ucs as ucs

# lưu đường dẫn file maze
maze_path = "D:/1LEARNING/CNTT/HK5/AI/repo/Lab1/input/level_1/input1.txt"

def find_start_goal(maze):
    # Tìm vị trí S và G trong ma trận
    start = None
    goal = None
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                start = (i, j)
            elif maze[i][j] == 'G':
                goal = (i, j)
    return start, goal

def load_maze(maze_path):
    # lưu điểm thưởng 
    mapping_bonus = {}
    # đọc file maze
    try:
        with open(maze_path, "r") as file:
            n = int(file.readline())
            for i in range(n):
                buff = file.readline()
                coordinates = buff.split(" ")
              
                x = int(coordinates[0])
                y = int(coordinates[1])
                val = int(coordinates[2])

                mapping_bonus[(x, y)] = val
            maze = [line.rstrip() for line in file.readlines()]      
        return maze, mapping_bonus
        
    except FileNotFoundError:
        print("Không tìm thấy file maze")
        exit()    

if __name__ == "__main__":
    # load maze và tìm điểm đầu cuối
    maze, mapping_bonus = load_maze(maze_path)
    start, goal = find_start_goal(maze)

    if start == None or goal == None:
        print("S and G not found")
    else:
        shortest_path_cost, path = ucs(maze, mapping_bonus, start, goal)
        if path is not None:
            print(f"Min Path Weight SG: {shortest_path_cost}")
            print("Path:")
            for node in path:
                x, y = node
                maze[x] = maze[x][:y] + '█' + maze[x][y + 1:]
            for line in maze:
                print(line)
        else:
            print("No path from S to G.")

