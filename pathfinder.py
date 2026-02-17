"""
GOOD PERFORMANCE TIME APP
AI Pathfinder - Uninformed Search Visualization
"""
import pygame, sys, time, random
from collections import deque
import heapq

ROWS, COLS = 15, 15
CELL = 44
MARGIN = 2
PANEL_W = 260
WIN_W = COLS * (CELL + MARGIN) + MARGIN + PANEL_W
WIN_H = ROWS * (CELL + MARGIN) + MARGIN + 80

BG=(15,17,26); GRID_BG=(22,26,40); C_EMPTY=(28,33,52); C_WALL=(60,60,80)
C_START=(52,152,219); C_TARGET=(46,204,113); C_FRONTIER=(231,76,60)
C_EXPLORED=(52,73,94); C_PATH=(241,196,15); C_DYNAMIC=(155,89,182)
C_TEXT=(220,220,230); C_DIM=(90,95,120); C_ACCENT=(52,152,219)
C_PANEL_BG=(18,21,34); C_BTN=(35,41,64); C_BTN_HOV=(52,152,219)
C_BTN_TXT=(210,215,230); C_TITLE=(241,196,15)

STEP_DELAY = 0.06
DYN_PROB   = 0.04
DLS_LIMIT  = 18

DIRECTIONS = [
    (-1, 0), ( 0, 1), ( 1, 0), ( 1, 1),
    ( 0,-1), (-1,-1), (-1, 1), ( 1,-1),
]

ALGORITHMS = ["BFS","DFS","UCS","DLS","IDDFS","Bidirectional"]

def reconstruct(parent, node):
    path = []
    while node is not None:
        path.append(node); node = parent[node]
    return list(reversed(path))

class Grid:
    def __init__(self):
        self.cells  = [[0]*COLS for _ in range(ROWS)]
        self.start  = (7, 1)
        self.target = (3, 9)
        self._place_default_walls()
    def _place_default_walls(self):
        for r,c in [(1,5),(2,5),(3,5),(4,5),(5,5),(6,5),(7,5),(8,5),(8,10),(8,11)]:
            self.cells[r][c] = 1
    def is_valid(self, r, c):
        return 0 <= r < ROWS and 0 <= c < COLS and self.cells[r][c] != 1
    def reset_to_default(self):
        self.cells = [[0]*COLS for _ in range(ROWS)]
        self._place_default_walls()

