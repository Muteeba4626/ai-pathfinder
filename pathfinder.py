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

# ── BFS ──────────────────────────────────────
def bfs(grid):
    start, target = grid.start, grid.target
    queue    = deque([start])
    parent   = {start: None}
    explored = set()
    frontier = {start}
    while queue:
        node = queue.popleft()
        frontier.discard(node)
        explored.add(node)
        if node == target:
            yield {"explored":explored,"frontier":frontier,
                   "path":reconstruct(parent,node),"done":True}
            return
        for dr,dc in DIRECTIONS:
            nb = (node[0]+dr, node[1]+dc)
            if grid.is_valid(*nb) and nb not in parent:
                parent[nb] = node
                queue.append(nb)
                frontier.add(nb)
        yield {"explored":explored,"frontier":frozenset(frontier),
               "path":[],"done":False}
    yield {"explored":explored,"frontier":frozenset(),"path":[],"done":True}

# ── DFS ──────────────────────────────────────
def dfs(grid):
    start, target = grid.start, grid.target
    stack    = [start]
    parent   = {start: None}
    explored = set()
    frontier = {start}
    while stack:
        node = stack.pop()
        if node in explored: continue
        frontier.discard(node)
        explored.add(node)
        if node == target:
            yield {"explored":explored,"frontier":frontier,
                   "path":reconstruct(parent,node),"done":True}
            return
        for dr,dc in reversed(DIRECTIONS):
            nb = (node[0]+dr, node[1]+dc)
            if grid.is_valid(*nb) and nb not in explored:
                if nb not in parent: parent[nb] = node
                stack.append(nb)
                frontier.add(nb)
        yield {"explored":explored,"frontier":frozenset(frontier),
               "path":[],"done":False}
    yield {"explored":explored,"frontier":frozenset(),"path":[],"done":True}


# ── UCS ──────────────────────────────────────
def ucs(grid):
    start, target = grid.start, grid.target
    heap     = [(0, start)]
    cost     = {start: 0}
    parent   = {start: None}
    explored = set()
    frontier = {start}
    while heap:
        g, node = heapq.heappop(heap)
        frontier.discard(node)
        if node in explored:
            yield {"explored":explored,"frontier":frozenset(frontier),
                   "path":[],"done":False}
            continue
        explored.add(node)
        if node == target:
            yield {"explored":explored,"frontier":frontier,
                   "path":reconstruct(parent,node),"done":True}
            return
        for dr,dc in DIRECTIONS:
            nb = (node[0]+dr, node[1]+dc)
            step_cost = 1.4 if (dr!=0 and dc!=0) else 1.0
            new_cost  = g + step_cost
            if grid.is_valid(*nb) and (nb not in cost or new_cost < cost[nb]):
                cost[nb] = new_cost; parent[nb] = node
                heapq.heappush(heap, (new_cost, nb))
                frontier.add(nb)
        yield {"explored":explored,"frontier":frozenset(frontier),
               "path":[],"done":False}
    yield {"explored":explored,"frontier":frozenset(),"path":[],"done":True}


# ── DLS ──────────────────────────────────────
def dls(grid, limit=DLS_LIMIT):
    start, target = grid.start, grid.target
    stack    = [(start, 0, {start: None})]
    vis      = {start}
    explored = set()
    frontier = {start}
    while stack:
        node, depth, pmap = stack.pop()
        frontier.discard(node)
        explored.add(node)
        if node == target:
            yield {"explored":explored,"frontier":frozenset(frontier),
                   "path":reconstruct(pmap,node),"done":True}
            return
        if depth < limit:
            for dr,dc in reversed(DIRECTIONS):
                nb = (node[0]+dr, node[1]+dc)
                if grid.is_valid(*nb) and nb not in vis:
                    vis.add(nb)
                    new_pmap = dict(pmap); new_pmap[nb] = node
                    stack.append((nb, depth+1, new_pmap))
                    frontier.add(nb)
        yield {"explored":explored,"frontier":frozenset(frontier),
               "path":[],"done":False}
    yield {"explored":explored,"frontier":frozenset(),"path":[],"done":True}

# ── IDDFS ─────────────────────────────────────
def iddfs(grid):
    start, target = grid.start, grid.target
    explored_total = set()
    frontier_set   = set()
    for depth_limit in range(1, ROWS*COLS):
        stack = [(start, 0, {start: None})]
        vis   = {start}
        explored = set()
        frontier = {start}
        while stack:
            node, depth, pmap = stack.pop()
            frontier.discard(node)
            explored.add(node)
            explored_total.add(node)
            if node == target:
                yield {"explored":explored_total,"frontier":frozenset(frontier),
                       "path":reconstruct(pmap,node),"done":True}
                return
            if depth < depth_limit:
                for dr,dc in reversed(DIRECTIONS):
                    nb = (node[0]+dr, node[1]+dc)
                    if grid.is_valid(*nb) and nb not in vis:
                        vis.add(nb)
                        new_pmap = dict(pmap); new_pmap[nb] = node
                        stack.append((nb, depth+1, new_pmap))
                        frontier.add(nb); frontier_set.add(nb)
            yield {"explored":explored_total,
                   "frontier":frozenset(frontier_set - explored_total),
                   "path":[],"done":False}
    yield {"explored":explored_total,"frontier":frozenset(),"path":[],"done":True}


# ── Bidirectional ─────────────────────────────
def bidirectional(grid):
    start, target = grid.start, grid.target
    fwd_queue   = deque([start]); bwd_queue   = deque([target])
    fwd_visited = {start: None};  bwd_visited = {target: None}
    explored    = set()
    frontier_set= {start, target}
    def build_path(meet):
        pf=[]; n=meet
        while n is not None: pf.append(n); n=fwd_visited[n]
        pf.reverse()
        pb=[]; n=bwd_visited[meet]
        while n is not None: pb.append(n); n=bwd_visited[n]
        return pf+pb
    while fwd_queue or bwd_queue:
        if fwd_queue:
            node = fwd_queue.popleft()
            frontier_set.discard(node); explored.add(node)
            if node in bwd_visited:
                yield {"explored":explored,"frontier":frozenset(frontier_set),
                       "path":build_path(node),"done":True}
                return
            for dr,dc in DIRECTIONS:
                nb=(node[0]+dr,node[1]+dc)
                if grid.is_valid(*nb) and nb not in fwd_visited:
                    fwd_visited[nb]=node; fwd_queue.append(nb); frontier_set.add(nb)
        if bwd_queue:
            node = bwd_queue.popleft()
            frontier_set.discard(node); explored.add(node)
            if node in fwd_visited:
                yield {"explored":explored,"frontier":frozenset(frontier_set),
                       "path":build_path(node),"done":True}
                return
            for dr,dc in DIRECTIONS:
                nb=(node[0]+dr,node[1]+dc)
                if grid.is_valid(*nb) and nb not in bwd_visited:
                    bwd_visited[nb]=node; bwd_queue.append(nb); frontier_set.add(nb)
        yield {"explored":explored,"frontier":frozenset(frontier_set),
               "path":[],"done":False}
    yield {"explored":explored,"frontier":frozenset(),"path":[],"done":True}

ALGO_MAP = {
    "BFS":bfs,"DFS":dfs,"UCS":ucs,
    "DLS":dls,"IDDFS":iddfs,"Bidirectional":bidirectional,
}

