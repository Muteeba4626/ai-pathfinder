# GOOD PERFORMANCE TIME APP
### AI Pathfinder – Uninformed Search Visualization

## Install & Run
```bash
pip install pygame
python pathfinder.py
```

## Algorithms
| # | Algorithm | Complete | Optimal |
|---|-----------|----------|---------|
| 1 | BFS | ✅ | ✅ |
| 2 | DFS | ✅ | ❌ |
| 3 | UCS | ✅ | ✅ |
| 4 | DLS | ❌ | ❌ |
| 5 | IDDFS | ✅ | ✅ |
| 6 | Bidirectional | ✅ | ~ |

## Movement Order (Clockwise + All Diagonals)
Up → Right → Down → Bottom-Right → Left → Top-Left → Top-Right → Bottom-Left

## Dynamic Obstacles
4% chance per step. Auto re-plans if path is blocked.

## Controls
- Click algorithm buttons to select
- ▶ START to run, ■ STOP to pause, ↺ RESET to clear
- Draw Walls / Set Start / Set Target with the editor buttons
