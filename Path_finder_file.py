import pygame
import sys
import random
import time
from queue import Queue,PriorityQueue

pygame.init()
pygame.font.init()

GRID_WIDTH = 750
CONTROLS_WIDTH = 100
width,height = GRID_WIDTH+CONTROLS_WIDTH,800
rows,cols = 20,20
cell_len = GRID_WIDTH//cols
obstacles = int(0.3*rows*cols)

white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
gray = (200,200,200)
light_blue = (173,216,230)

font = pygame.font.SysFont('Arial',16)
large_font = pygame.font.SysFont('Arial',32)
grid = [[0 for _ in range(cols)] for _ in range(rows)]  
# 0=empty,1=obstacle,2=start,3=goal

# Set unique obstacles
for _ in range(obstacles):
    while True:
        row,col = random.randint(0,rows-1),random.randint(0,cols-1)
        if grid[row][col] == 0:
            grid[row][col] = 1
            break

# Set start and goal positions
while True:
    start = (random.randint(0,rows-1),random.randint(0,cols-1))
    goal = (random.randint(0, rows-1),random.randint(0,cols-1))
    if (grid[start[0]][start[1]] != 1 and grid[goal[0]][goal[1]] != 1 and start != goal):
        grid[start[0]][start[1]] = 2
        grid[goal[0]][goal[1]] = 3
        break

# Pygame Window
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pathfinder's Quest!")

# Visualization states
VISIT_COLOR = light_blue
PATH_COLOR = blue
START_COLOR = green
GOAL_COLOR = red
OBSTACLE_COLOR = black

# Draw the grid
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            color = white
            if grid[row][col] == 1:
                color = OBSTACLE_COLOR
            elif grid[row][col] == 2:
                color = START_COLOR
            elif grid[row][col] == 3:
                color = GOAL_COLOR
            pygame.draw.rect(screen,color,(col*cell_len, row*cell_len, cell_len, cell_len))        # for rectangles
            pygame.draw.rect(screen,black,(col*cell_len, row*cell_len, cell_len, cell_len),1)      # for border

# Draw visited nodes
def draw_visited(visited):
    for (row,col) in visited:
        if grid[row][col] not in [2,3]:                              # Don't overwrite start/goal
            pygame.draw.rect(screen,VISIT_COLOR,(col*cell_len, row*cell_len, cell_len, cell_len))
            pygame.draw.rect(screen,black,(col*cell_len, row*cell_len, cell_len, cell_len),1)

# Draw the path
def draw_path(path):
    if path:
        for (row,col) in path:
            if grid[row][col] not in [2,3]:                         # Don't overwrite start/goal
                pygame.draw.rect(screen,PATH_COLOR,(col*cell_len, row*cell_len, cell_len, cell_len))
                pygame.draw.rect(screen,black,(col*cell_len, row*cell_len, cell_len, cell_len),1)

# Draw the info panel
def draw_info_panel(algorithm,time_taken,path_length,visited_count):
    pygame.draw.rect(screen,gray,(0,height-60,width,60))
    algorithm_text = f"Algorithm: {algorithm}" if algorithm else "Press B(BFS), D(DFS), or A(A*)"
    time_text = f"Time: {time_taken:.4f}s" if time_taken else "Time: -"
    path_text = f"Path: {path_length} steps" if path_length else "Path: -"
    visited_text = f"Visited: {visited_count} nodes" if visited_count else "Visited: -"
    texts = [font.render(algorithm_text,True,black),
             font.render(time_text,True,black),
             font.render(path_text,True,black),
             font.render(visited_text,True,black)]
    for i,text in enumerate(texts):
        screen.blit(text,(20+i*200,height-50))

# Search Algorithms with visualization
def bfs(start,goal,visualize=False):
    start_time = time.time()
    queue = Queue()
    queue.put((start,[start]))
    visited = set()
    visited_order = []
    
    visited.add(start)
    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        (current,path) = queue.get()
        visited_order.append(current)
        
        if visualize:
            screen.fill(white)
            draw_grid()
            draw_visited(visited_order)
            draw_path(path)
            draw_info_panel("BFS",time.time()-start_time,len(path) if current == goal else 0,len(visited_order))
            pygame.display.flip()
            pygame.time.delay(50)
        
        if current == goal:
            return path,time.time()-start_time,len(visited_order)
        
        for (dr,dc) in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            neighbor = (current[0]+dr,current[1]+dc)
            if 0<=neighbor[0]<rows and 0<=neighbor[1]<cols:
                if grid[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                    visited.add(neighbor)
                    queue.put((neighbor,path+[neighbor]))
    
    return None,time.time()-start_time,len(visited_order)

def dfs(start,goal,visualize=False):
    start_time = time.time()
    stack = [(start,[start])]
    visited = set()
    visited_order = []
    
    visited.add(start)
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        (current,path) = stack.pop()
        visited_order.append(current)
        
        if visualize:
            screen.fill(white)
            draw_grid()
            draw_visited(visited_order)
            draw_path(path)
            draw_info_panel("DFS",time.time()-start_time,len(path) if current == goal else 0,len(visited_order))
            pygame.display.flip()
            pygame.time.delay(50)
        
        if current == goal:
            return path,time.time()-start_time,len(visited_order)
        
        # Reverse the order to explore in consistent direction and moreover (diagonal move cover more distance)
        for (dr,dc) in reversed([(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]):
            neighbor = (current[0]+dr,current[1]+dc)
            if 0<=neighbor[0]<rows and 0<=neighbor[1]<cols:
                if grid[neighbor[0]][neighbor[1]] != 1 and neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor,path+[neighbor]))
    
    return None,time.time()-start_time,len(visited_order)

def a_star(start,goal,visualize=False):
    start_time = time.time()
    def heuristic(a,b):
        # Euclidean distance
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5
    
    pq = PriorityQueue()
    pq.put((0,start,[start]))
    visited_order = []
    cost_so_far = {start:0}
    
    while not pq.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        (priority,current,path) = pq.get()
        visited_order.append(current)
        
        if visualize:
            screen.fill(white)
            draw_grid()
            draw_visited(visited_order)
            draw_path(path)
            draw_info_panel("A*",time.time()-start_time,len(path) if current == goal else 0,len(visited_order))
            pygame.display.flip()
            pygame.time.delay(50)
        
        if current == goal:
            return path,time.time()-start_time,len(visited_order)
        
        for (dr,dc) in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            neighbor = (current[0]+dr,current[1]+dc)
            if 0<=neighbor[0]<rows and 0<=neighbor[1]<cols:
                if grid[neighbor[0]][neighbor[1]] != 1:
                    new_cost = cost_so_far[current]+1
                    if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                        cost_so_far[neighbor] = new_cost
                        priority = cost_so_far[neighbor] + heuristic(neighbor,goal)
                        pq.put((priority,neighbor,path+[neighbor]))
    
    return None,time.time()-start_time,len(visited_order)

def compare_algorithms():
    results = []
    path,time_taken,visited = bfs(start,goal,False)
    results.append(("BFS",time_taken,len(path) if path else 0,visited))
    
    path,time_taken,visited = dfs(start,goal,False)
    results.append(("DFS",time_taken,len(path) if path else 0,visited))
    
    path,time_taken,visited = a_star(start,goal,False)
    results.append(("A*",time_taken,len(path) if path else 0,visited))
    
    best_time = min(results,key=lambda x:x[1])[0]
    best_path = min(results,key=lambda x:x[2])[0] if any(x[2]>0 for x in results) else "N/A"
    best_visited = min(results,key=lambda x:x[3])[0]
    
    screen.fill(white)
    title = large_font.render("Algorithm Comparison Results",True,black)
    screen.blit(title,((width//2)-(title.get_width()//2),20))
    
    y_pos = 70
    for name,t,pl,vis in results:
        text = font.render(f"{name}: Time={t:.4f}s, Path={pl}, Visited={vis}",True,black)
        screen.blit(text,((width//2) - (text.get_width()//2),y_pos))
        y_pos += 30
    
    conclusion = large_font.render(f"Best: Time={best_time}, Path={best_path}, Visited={best_visited}",True,blue)
    screen.blit(conclusion,((width//2) - (conclusion.get_width()//2),y_pos+40))
    pygame.display.flip()
    
    # Wait for user to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Main Game Loop
def main():
    global screen,width,height,cell_len
    running = True
    path = None
    algorithm = None
    time_taken = 0
    visited_count = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    path,time_taken,visited_count = bfs(start,goal,True)
                    algorithm = "BFS"
                elif event.key == pygame.K_d:
                    path,time_taken,visited_count = dfs(start,goal,True)
                    algorithm = "DFS"
                elif event.key == pygame.K_a:
                    path,time_taken,visited_count = a_star(start,goal,True)
                    algorithm = "A*"
                elif event.key == pygame.K_c:
                    compare_algorithms()
                elif event.key == pygame.K_r:
                    path = None
                    algorithm = None
                    time_taken = 0
                    visited_count = 0
        
        screen.fill(white)
        draw_grid()
        if algorithm:
            draw_path(path)
        pygame.draw.rect(screen,gray,(GRID_WIDTH-9.5,0,CONTROLS_WIDTH+9.5,height-50))
        instructions = ["Controls:",
                        "B - Run BFS",
                        "D - Run DFS",
                        "A - Run A*",
                        "C - Compare",
                        "R - Reset"]
        for i,text in enumerate(instructions):
            text_surface = font.render(text,True,black)
            screen.blit(text_surface,(GRID_WIDTH+12,300+i*25))
        draw_info_panel(algorithm,time_taken,len(path) if path else 0,visited_count)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()