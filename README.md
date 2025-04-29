# Pathfinding Algorithms Visualization

## Project Overview
This project compares three fundamental pathfinding algorithms—Breadth-First Search (BFS), Depth-First Search (DFS), and A*—in a grid-based environment. It features an interactive visualization tool built with Pygame to demonstrate their efficiency, exploration patterns, and path optimality.

## Key Features
- **Interactive Grid**: 20x20 grid with 30% randomly placed obstacles, a start point, and a goal.
- **Algorithm Implementations**:
  - **BFS**: Guarantees the shortest path but explores many nodes.
  - **DFS**: Memory-efficient but may yield suboptimal paths.
  - **A***: Balances speed and optimality using a heuristic (Euclidean distance).
- **Real-Time Visualization**: Watch each algorithm explore the grid step-by-step.
- **Performance Metrics**: Compare execution time, path length, and nodes visited.

## How to Use
- **B**: Run BFS  
- **D**: Run DFS  
- **A**: Run A*  
- **C**: Compare algorithms  
- **R**: Reset the grid  

## Results
| Algorithm | Path Optimality | Exploration Pattern | Best Use Case |
|-----------|----------------|----------------------|---------------|
| BFS       | Shortest path  | Uniform expansion    | Unweighted grids where shortest path is critical |
| DFS       | Suboptimal     | Deep exploration     | Memory-constrained scenarios |
| A*        | Shortest path  | Heuristic-guided     | Weighted/unweighted grids for speed and optimality |

## Future Enhancements
1. Add Dijkstra’s Algorithm for weighted grids.  
2. Introduce dynamic obstacles for real-time challenges.  
3. Include adjustable heuristics (Manhattan vs. Euclidean).  
4. Add zoom/pan functionality for larger grids.  

## Technologies Used
- Python  
- Pygame  

## References
- Pygame Documentation: [https://www.pygame.org/docs/](https://www.pygame.org/docs/)   

This project serves as an educational tool to understand algorithmic trade-offs in pathfinding. Contributions and feedback are welcome!
