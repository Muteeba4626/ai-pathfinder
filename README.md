# GOOD PERFORMANCE TIME APP
### AI Pathfinder using Uninformed Search Visualization

## Install & Run
```bash
pip install pygame
python pathfinder.py
```

## Algorithms
| # | Algorithm | Complete | Optimal |
|---|-----------|----------|---------|
| 1 | BFS | yes | yes |
| 2 | DFS | yes | no |
| 3 | UCS | yes | yes |
| 4 | DLS | no | no |
| 5 | IDDFS | yes | yes |
| 6 | Bidirectional | no | ~ |

## Movement Order 
Up → Right → Down → Bottom-Right → Left → Top-Left → Top-Right → Bottom-Left

## Dynamic Obstacles
4% chance per step. Auto re-plans if path is blocked.

## Controls
- Click algorithm buttons to select
- Press START button to run, STOP button  to pause and  RESET button to clear
- Draw Walls / Set Start / Set Target with the editor buttons
