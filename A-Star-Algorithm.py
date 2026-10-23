
import heapq

# Name and the last 4 digits of the student number
# Mobina Zangooie 1010
# Fateme Gheidy   1014

start = (1, 1)
goal = (1, 7)
bridge = 4
river = 2

# 0 represents the wall
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

def heuristic(a, b):
    # a simple manhattan distance heuristic
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    Path_reconstruction = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    total_cost = 0
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in Path_reconstruction:
                path.append(current)
                current = Path_reconstruction[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        
        for direction in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # left, down, right, up
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] == 1:
                tentative_g_score = g_score[current] + 1
                tentative_cost = 1
                
                if (current == (3, 5) and neighbor == (3, 6)) or (current == (3, 5) and neighbor == (3, 7)):
                    tentative_g_score += bridge
                    tentative_cost += bridge
                
                if (current == (5, 9) and neighbor == (6, 9)) or (current == (5, 9) and neighbor == (3, 9)):
                    tentative_g_score += river
                    tentative_cost += river
                
                total_cost += tentative_cost
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    Path_reconstruction[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None, float('inf')

def filter_path(path):
    return [(i, j) for i, j in path if i % 2 == 1 and j % 2 == 1]

def convert_to_5x5_path(path):
    return [((i - 1) // 2 , (j - 1) // 2 ) for i, j in path]

def calculate_filtered_path_cost(path):
    cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        neighbor = path[i + 1]
        cost += 1
        
        if (current == (3, 5) and neighbor == (3, 6)) or (current == (3, 5) and neighbor == (3, 7)):
            cost += bridge
        
        if (current == (5, 9) and neighbor == (6, 9)) or (current == (5, 9) and neighbor == (3, 9)):
            cost += river
    return cost

path, total_cost = a_star(maze, start, goal)
filtered_path = filter_path(path)
filtered_path_cost = calculate_filtered_path_cost(filtered_path)
path_5x5 = convert_to_5x5_path(filtered_path)

#print("11x11 Path:", filtered_path)
print("5x5 Path:", path_5x5)
#print("Total cost:", total_cost)
print("Filtered path cost:", filtered_path_cost-1)
