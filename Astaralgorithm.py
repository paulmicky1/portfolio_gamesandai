
import heapq

def get_neighbors(node, grid):
    neighbors = []
    x, y = node
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if (nx, ny) in grid and grid[(nx, ny)] != 1:  # Ensure it's a valid, non-blocked node
            neighbors.append((nx, ny))
    
    return neighbors

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance heuristic

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:
            return []  # No valid path found
    path.append(start)
    path.reverse()
    return path

def a_star(start, goal, grid):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in grid}
    g_score[start] = 0
    f_score = {node: float('inf') for node in grid}
    f_score[start] = heuristic(start, goal)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            return reconstruct_path(came_from, start, goal)
        
        for neighbor in get_neighbors(current, grid):
            tentative_g = g_score[current] + 1
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []  # No path found

# Example usage
grid = {(x, y): 0 for x in range(5) for y in range(5)}  # 5x5 grid
grid[(2, 2)] = 1  # Adding an obstacle
start = (0, 0)
goal = (4, 4)
path = a_star(start, goal, grid)
print("Path:", path)
