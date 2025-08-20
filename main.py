# AI Search Algorithms for N-Puzzle - Pythonista Implementation
# Taller: Buscadores IA en Móvil con Python
# Adrián Fernando Gaitán Londoño

import ui
import time
import threading
from typing import Any, Iterable, Optional, List, Tuple
from math import inf


# ============================================================================
# ESTRUCTURAS DE DATOS (implementadas manualmente)
# ============================================================================

class Stack:
    def __init__(self):
        self._a = []

    def push(self, x):
        self._a.append(x)

    def pop(self):
        if not self._a:
            raise IndexError("pop from empty Stack")
        return self._a.pop()

    def is_empty(self):
        return not self._a

    def __len__(self):
        return len(self._a)


class Queue:
    def __init__(self):
        self._a = []

    def enqueue(self, x):
        self._a.append(x)

    def dequeue(self):
        if not self._a:
            raise IndexError("dequeue from empty Queue")
        return self._a.pop(0)

    def is_empty(self):
        return not self._a

    def __len__(self):
        return len(self._a)


class MinHeap:
    def __init__(self):
        self._heap = []

    def push(self, item):
        self._heap.append(item)
        self._bubble_up(len(self._heap) - 1)

    def pop(self):
        if not self._heap:
            raise IndexError("pop from empty MinHeap")
        if len(self._heap) == 1:
            return self._heap.pop()

        result = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._bubble_down(0)
        return result

    def is_empty(self):
        return not self._heap

    def __len__(self):
        return len(self._heap)

    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx] >= self._heap[parent]:
                break
            self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
            idx = parent

    def _bubble_down(self, idx):
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < len(self._heap) and self._heap[left] < self._heap[smallest]:
                smallest = left
            if right < len(self._heap) and self._heap[right] < self._heap[smallest]:
                smallest = right

            if smallest == idx:
                break

            self._heap[idx], self._heap[smallest] = self._heap[smallest], self._heap[idx]
            idx = smallest


# ============================================================================
# ABSTRACCIONES: State, Problem, Node
# ============================================================================

class State:
    def key(self) -> Any:
        raise NotImplementedError

    def __hash__(self):
        return hash(self.key())

    def __eq__(self, other):
        return isinstance(other, State) and self.key() == other.key()


class Problem:
    def initial_state(self) -> State:
        raise NotImplementedError

    def is_goal(self, s: State) -> bool:
        raise NotImplementedError

    def actions(self, s: State) -> Iterable[Any]:
        raise NotImplementedError

    def result(self, s: State, a: Any) -> State:
        raise NotImplementedError

    def step_cost(self, s: State, a: Any, sp: State) -> float:
        return 1.0


class Node:
    __slots__ = ("state", "parent", "action", "g", "depth")

    def __init__(self, state: State, parent: Optional['Node'] = None, action=None, g: float = 0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self, problem: Problem):
        for a in problem.actions(self.state):
            sp = problem.result(self.state, a)
            yield Node(sp, self, a, self.g + problem.step_cost(self.state, a, sp))


def reconstruct_path(n: Node) -> List[Tuple[Any, State]]:
    path = []
    while n:
        path.append((n.action, n.state))
        n = n.parent
    return list(reversed(path))


# ============================================================================
# PROBLEMA: 8-PUZZLE
# ============================================================================

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
GOAL_POS = {v: i for i, v in enumerate(GOAL)}


class PuzzleState(State):
    __slots__ = ("tiles",)

    def __init__(self, tiles):
        self.tiles = tuple(tiles)

    def key(self):
        return self.tiles

    def __repr__(self):
        return f"PuzzleState{self.tiles}"


class Puzzle(Problem):
    def __init__(self, start):
        self.start = PuzzleState(start)

    def initial_state(self) -> State:
        return self.start

    def is_goal(self, s: PuzzleState) -> bool:
        return s.tiles == GOAL

    def actions(self, s: PuzzleState):
        i = s.tiles.index(0)
        x, y = divmod(i, 3)
        for dx, dy, a in ((1, 0, "DOWN"), (-1, 0, "UP"), (0, 1, "RIGHT"), (0, -1, "LEFT")):
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                yield a

    def result(self, s: PuzzleState, a):
        delta = {"DOWN": (1, 0), "UP": (-1, 0), "RIGHT": (0, 1), "LEFT": (0, -1)}[a]
        i = s.tiles.index(0)
        x, y = divmod(i, 3)
        nx, ny = x + delta[0], y + delta[1]
        j = nx * 3 + ny
        tiles = list(s.tiles)
        tiles[i], tiles[j] = tiles[j], tiles[i]
        return PuzzleState(tiles)


# ============================================================================
# HEURÍSTICAS
# ============================================================================

def misplaced(s: PuzzleState) -> int:
    """Heurística: número de fichas fuera de lugar"""
    return sum(1 for i, v in enumerate(s.tiles) if v != 0 and v != GOAL[i])


def manhattan(s: PuzzleState) -> int:
    """Heurística: distancia Manhattan total"""
    dist = 0
    for i, v in enumerate(s.tiles):
        if v == 0:
            continue
        gi = GOAL_POS[v]
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(gi, 3)
        dist += abs(x1 - x2) + abs(y1 - y2)
    return dist


def linear_conflict(s: PuzzleState) -> int:
    """Heurística extra: conflicto lineal + Manhattan"""
    base = manhattan(s)
    conflicts = 0

    # Conflictos en filas
    for row in range(3):
        for col in range(3):
            pos = row * 3 + col
            tile = s.tiles[pos]
            if tile == 0:
                continue
            goal_pos = GOAL_POS[tile]
            goal_row, goal_col = divmod(goal_pos, 3)

            if row == goal_row:
                for other_col in range(col + 1, 3):
                    other_pos = row * 3 + other_col
                    other_tile = s.tiles[other_pos]
                    if other_tile == 0:
                        continue
                    other_goal_pos = GOAL_POS[other_tile]
                    other_goal_row, other_goal_col = divmod(other_goal_pos, 3)

                    if other_goal_row == row and other_goal_col < goal_col:
                        conflicts += 1

    # Conflictos en columnas
    for col in range(3):
        for row in range(3):
            pos = row * 3 + col
            tile = s.tiles[pos]
            if tile == 0:
                continue
            goal_pos = GOAL_POS[tile]
            goal_row, goal_col = divmod(goal_pos, 3)

            if col == goal_col:
                for other_row in range(row + 1, 3):
                    other_pos = other_row * 3 + col
                    other_tile = s.tiles[other_pos]
                    if other_tile == 0:
                        continue
                    other_goal_pos = GOAL_POS[other_tile]
                    other_goal_row, other_goal_col = divmod(other_goal_pos, 3)

                    if other_goal_col == col and other_goal_row < goal_row:
                        conflicts += 1

    return base + 2 * conflicts


# ============================================================================
# PRIORITY QUEUE para algoritmos informados
# ============================================================================

class PriorityQueue:
    def __init__(self):
        self._h = MinHeap()
        self._t = 0

    def push(self, priority, item):
        self._t += 1
        self._h.push((priority, self._t, item))

    def pop(self):
        return self._h.pop()[2]

    def is_empty(self):
        return self._h.is_empty()

    def __len__(self):
        return len(self._h)


# ============================================================================
# ALGORITMOS DE BÚSQUEDA
# ============================================================================

def BFS(problem: Problem):
    """Búsqueda en amplitud"""
    frontier = Queue()
    frontier.enqueue(Node(problem.initial_state()))
    explored = set()
    expanded = 0

    while not frontier.is_empty():
        n = frontier.dequeue()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        if n.state in explored:
            continue
        explored.add(n.state)
        expanded += 1
        for c in n.expand(problem):
            frontier.enqueue(c)

    return None, expanded


def DFS(problem: Problem, depth_limit=None):
    """Búsqueda en profundidad"""
    frontier = Stack()
    frontier.push(Node(problem.initial_state()))
    explored = set()
    expanded = 0

    while not frontier.is_empty():
        n = frontier.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        if n.state in explored:
            continue
        if depth_limit is not None and n.depth > depth_limit:
            continue
        explored.add(n.state)
        expanded += 1
        for c in n.expand(problem):
            frontier.push(c)

    return None, expanded


def UCS(problem: Problem):
    """Búsqueda de costo uniforme"""
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(0.0, start)
    best = {start.state: 0.0}
    expanded = 0

    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(c.g, c)

    return None, expanded


def Greedy(problem: Problem, h):
    """Búsqueda voraz"""
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(h(start.state), start)
    seen = set()
    expanded = 0

    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        if n.state in seen:
            continue
        seen.add(n.state)
        expanded += 1
        for c in n.expand(problem):
            pq.push(h(c.state), c)

    return None, expanded


def A_star(problem: Problem, h):
    """A* search"""
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(h(start.state) + start.g, start)
    best = {start.state: 0.0}
    expanded = 0

    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            f = c.g + h(c.state)
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(f, c)

    return None, expanded


def Weighted_A_star(problem: Problem, h, w=1.5):
    """Weighted A* (extra)"""
    pq = PriorityQueue()
    start = Node(problem.initial_state())
    pq.push(w * h(start.state) + start.g, start)
    best = {start.state: 0.0}
    expanded = 0

    while not pq.is_empty():
        n = pq.pop()
        if problem.is_goal(n.state):
            return reconstruct_path(n), expanded
        expanded += 1
        for c in n.expand(problem):
            f = c.g + w * h(c.state)
            if c.state not in best or c.g < best[c.state]:
                best[c.state] = c.g
                pq.push(f, c)

    return None, expanded


def IDA_star(problem: Problem, h):
    """Iterative Deepening A*"""
    start = Node(problem.initial_state())
    bound = h(start.state)
    expanded_total = 0

    def dfs_limited(n, g, bound):
        nonlocal expanded_total
        f = g + h(n.state)
        if f > bound:
            return f, None
        if problem.is_goal(n.state):
            return f, reconstruct_path(n)
        m = inf
        for c in n.expand(problem):
            expanded_total += 1
            t, sol = dfs_limited(c, g + (c.g - n.g), bound)
            if sol is not None:
                return t, sol
            if t < m:
                m = t
        return m, None

    while True:
        t, sol = dfs_limited(start, 0, bound)
        if sol is not None:
            return sol, expanded_total
        if t == float("inf"):
            return None, expanded_total
        bound = t


# ============================================================================
# INTERFAZ GRÁFICA CON PYTHONISTA
# ============================================================================

class PuzzleView(ui.View):
    def __init__(self):
        self.name = 'AI Search - 8-Puzzle'
        self.background_color = '#f0f0f0'

        # Estado actual del puzzle
        self.current_state = (1, 4, 2, 7, 5, 3, 0, 8, 6)  # Estado inicial
        self.solution_path = None
        self.animation_running = False
        self.animation_step = 0

        self.setup_ui()

    def setup_ui(self):
        # Panel principal
        main_view = ui.View(frame=(0, 0, 600, 1000))
        main_view.background_color = 'white'
        self.add_subview(main_view)

        # Título
        title_label = ui.Label()
        title_label.text = 'AI Search - 8-Puzzle'
        title_label.font = ('Arial', 28)
        title_label.text_color = 'black'
        title_label.alignment = ui.ALIGN_CENTER
        title_label.frame = (0, 20, 600, 40)
        main_view.add_subview(title_label)

        # Grid del puzzle - Mucho más grande
        self.grid_view = ui.View(frame=(75, 80, 450, 450))
        self.grid_view.background_color = '#333333'
        main_view.add_subview(self.grid_view)

        # Crear tiles 
        self.tile_labels = []
        for i in range(9):
            tile = ui.Label()
            tile.font = ('Arial', 36)
            tile.text_color = 'white'
            tile.background_color = '#4CAF50'
            tile.alignment = ui.ALIGN_CENTER
            tile.corner_radius = 12
            self.tile_labels.append(tile)
            self.grid_view.add_subview(tile)

        self.update_puzzle_display()

        # Selector de algoritmo
        algo_label = ui.Label()
        algo_label.text = 'Algoritmo:'
        algo_label.font = ('Arial', 20)
        algo_label.frame = (30, 560, 150, 40)
        main_view.add_subview(algo_label)

        self.algorithm_selector = ui.SegmentedControl()
        self.algorithm_selector.segments = ['BFS', 'DFS', 'A*', 'Greedy', 'IDA*']
        self.algorithm_selector.selected_index = 2  # A* por defecto
        self.algorithm_selector.frame = (30, 600, 540, 40)
        main_view.add_subview(self.algorithm_selector)

        # Selector de heurística
        heur_label = ui.Label()
        heur_label.text = 'Heurística:'
        heur_label.font = ('Arial', 20)
        heur_label.frame = (30, 650, 150, 40)
        main_view.add_subview(heur_label)

        self.heuristic_selector = ui.SegmentedControl()
        self.heuristic_selector.segments = ['Manhattan', 'Misplaced', 'Linear Conflict']
        self.heuristic_selector.selected_index = 0  # Manhattan por defecto
        self.heuristic_selector.frame = (30, 690, 540, 40)
        main_view.add_subview(self.heuristic_selector)

        # Botones de control
        solve_button = ui.Button()
        solve_button.title = 'Resolver'
        solve_button.background_color = '#2196F3'
        solve_button.tint_color = 'white'
        solve_button.corner_radius = 12
        solve_button.font = ('Arial', 18)
        solve_button.frame = (30, 750, 120, 50)
        solve_button.action = self.solve_puzzle
        main_view.add_subview(solve_button)

        shuffle_button = ui.Button()
        shuffle_button.title = 'Mezclar'
        shuffle_button.background_color = '#FF9800'
        shuffle_button.tint_color = 'white'
        shuffle_button.corner_radius = 12
        shuffle_button.font = ('Arial', 18)
        shuffle_button.frame = (170, 750, 120, 50)
        shuffle_button.action = self.shuffle_puzzle
        main_view.add_subview(shuffle_button)

        animate_button = ui.Button()
        animate_button.title = 'Animar'
        animate_button.background_color = '#4CAF50'
        animate_button.tint_color = 'white'
        animate_button.corner_radius = 12
        animate_button.font = ('Arial', 18)
        animate_button.frame = (310, 750, 120, 50)
        animate_button.action = self.animate_solution
        main_view.add_subview(animate_button)

        reset_button = ui.Button()
        reset_button.title = 'Reset'
        reset_button.background_color = '#F44336'
        reset_button.tint_color = 'white'
        reset_button.corner_radius = 12
        reset_button.font = ('Arial', 18)
        reset_button.frame = (450, 750, 120, 50)
        reset_button.action = self.reset_puzzle
        main_view.add_subview(reset_button)

        # Área de resultados - Más grande
        self.results_text = ui.TextView()
        self.results_text.frame = (30, 820, 540, 160)
        self.results_text.background_color = '#f8f8f8'
        self.results_text.font = ('Courier', 16)
        self.results_text.editable = False
        self.results_text.text = 'Selecciona un algoritmo y presiona "Resolver"'
        main_view.add_subview(self.results_text)

    def update_puzzle_display(self):
        """Actualiza la visualización del puzzle"""
        for i, value in enumerate(self.current_state):
            x = (i % 3) * 150 + 5  # Tiles más grandes (150x150 en lugar de 100x100)
            y = (i // 3) * 150 + 5
            self.tile_labels[i].frame = (x, y, 140, 140)  # 140x140 con margen de 5px

            if value == 0:
                self.tile_labels[i].text = ''
                self.tile_labels[i].background_color = '#333333'
            else:
                self.tile_labels[i].text = str(value)
                self.tile_labels[i].background_color = '#4CAF50'

    def get_selected_heuristic(self):
        """Retorna la función heurística seleccionada"""
        heuristics = [manhattan, misplaced, linear_conflict]
        return heuristics[self.heuristic_selector.selected_index]

    def solve_puzzle(self, sender):
        """Resuelve el puzzle con el algoritmo seleccionado"""
        if self.animation_running:
            return

        problem = Puzzle(self.current_state)
        algo_name = self.algorithm_selector.segments[self.algorithm_selector.selected_index]
        h = self.get_selected_heuristic()

        self.results_text.text = f"Ejecutando {algo_name}..."

        # Ejecutar en hilo separado para no bloquear UI
        def solve_thread():
            try:
                start_time = time.time()

                if algo_name == 'BFS':
                    result, expanded = BFS(problem)
                elif algo_name == 'DFS':
                    result, expanded = DFS(problem, depth_limit=20)
                elif algo_name == 'A*':
                    result, expanded = A_star(problem, h)
                elif algo_name == 'Greedy':
                    result, expanded = Greedy(problem, h)
                elif algo_name == 'IDA*':
                    result, expanded = IDA_star(problem, h)

                elapsed = time.time() - start_time

                if result is None:
                    self.results_text.text = f"{algo_name}: No se encontró solución\nNodos expandidos: {expanded}\nTiempo: {elapsed:.3f}s"
                else:
                    self.solution_path = result
                    steps = [a for a, _ in result][1:]  # excluir None inicial
                    depth = len(steps)

                    heur_name = self.heuristic_selector.segments[self.heuristic_selector.selected_index]
                    self.results_text.text = f"{algo_name} ({heur_name}):\n✅ Solución encontrada!\nPasos: {depth}\nNodos expandidos: {expanded}\nTiempo: {elapsed:.3f}s"

            except Exception as e:
                self.results_text.text = f"Error: {str(e)}"

        threading.Thread(target=solve_thread).start()

    def shuffle_puzzle(self, sender):
        """Mezcla el puzzle aleatoriamente"""
        import random
        if self.animation_running:
            return

        # Generar estado aleatorio solucionable
        tiles = list(range(9))
        while True:
            random.shuffle(tiles)
            if self.is_solvable(tiles):
                break

        self.current_state = tuple(tiles)
        self.update_puzzle_display()
        self.solution_path = None
        self.results_text.text = 'Puzzle mezclado. Selecciona algoritmo y resuelve!'

    def is_solvable(self, tiles):
        """Verifica si el puzzle es solucionable"""
        inversions = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if tiles[i] != 0 and tiles[j] != 0 and tiles[i] > tiles[j]:
                    inversions += 1
        return inversions % 2 == 0

    def animate_solution(self, sender):
        """Anima la solución paso a paso"""
        if not self.solution_path or self.animation_running:
            return

        self.animation_running = True
        self.animation_step = 0

        def animate_step():
            if self.animation_step >= len(self.solution_path):
                self.animation_running = False
                return

            _, state = self.solution_path[self.animation_step]
            self.current_state = state.tiles
            self.update_puzzle_display()
            self.animation_step += 1

            if self.animation_running:
                self.after_delay(0.5, animate_step)

        animate_step()

    def reset_puzzle(self, sender):
        """Resetea el puzzle al estado inicial"""
        if self.animation_running:
            return

        self.current_state = (1, 4, 2, 7, 5, 3, 0, 8, 6)
        self.update_puzzle_display()
        self.solution_path = None
        self.results_text.text = 'Puzzle reseteado. ¡Listo para resolver!'

    def after_delay(self, delay, func):
        """Ejecuta función después de un delay"""

        def delayed():
            time.sleep(delay)
            func()

        threading.Thread(target=delayed).start()


# ============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# ============================================================================

if __name__ == '__main__':
    # Crear y mostrar la aplicación
    app = PuzzleView()
    app.present('fullscreen')
