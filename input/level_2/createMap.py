import os
import random

def load_maze(maze_path):
    maze_path = os.path.join(maze_path)
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

def save_maze(maze, mapping_bonus, output_file):
    try:
        with open(output_file, "w") as file:
            # Ghi số hàng và cột của ma trận mê cung
            file.write(f"{len(mapping_bonus)}\n")
            
            # Ghi thông tin về điểm thưởng
            for coordinates, value in mapping_bonus.items():
                x, y = coordinates
                maze[y] = maze[y][:x] + '+' + maze[y][x + 1:]
                file.write(f"{x} {y} {value}\n")
            
            # Ghi mê cung
            for line in maze:
                file.write(line + "\n")
                
        print(f"Đã lưu mê cung và điểm thưởng vào tệp {output_file}")
    except Exception as e:
        print(f"Có lỗi xảy ra khi lưu file: {e}")

# get current file directory
current_dir = os.path.dirname(os.path.abspath(__file__))

maze, mapping_bonus = load_maze(current_dir + "/input3.txt")

# add to list
for i in range(10):
    mapping_bonus[(random.randint(1, len(maze[0]) - 2), random.randint(1, len(maze) - 2))] = random.randint(-10, 0)

save_maze(maze, mapping_bonus, current_dir + "/input3_3.txt")

