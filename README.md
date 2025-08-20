# AI Search Algorithms on Mobile with Python - 8-Puzzle

**Artificial Intelligence Workshop - Search Algorithms Implementation**

**Author:** Adrián Fernando Gaitán Londoño

## Project Description

This project implements an interactive mobile application to solve the classic 8-puzzle problem using different Artificial Intelligence search algorithms. The application is developed in Python using the Pythonista framework for iOS devices, providing an intuitive graphical interface for experimenting with various search algorithms.

## Key Features

### Implemented Search Algorithms
- **BFS (Breadth-First Search)** - Breadth-First Search
- **DFS (Depth-First Search)** - Depth-First Search
- **A*** - A Star Algorithm
- **Greedy** - Greedy Search
- **IDA*** - Iterative Deepening A*

### Heuristic Functions
- **Manhattan Distance** - Manhattan Distance
- **Misplaced Tiles** - Misplaced Tiles Count
- **Linear Conflict** - Linear Conflict (Advanced Heuristic)

### Application Features
- Interactive graphical interface with 3x3 grid
- Algorithm and heuristic selection
- Step-by-step solution animation
- Random puzzle shuffling
- Performance statistics (expanded nodes, execution time)
- Solution path visualization

## Runtime Environment

### System Requirements

#### Primary Platform: iOS with Pythonista
- **Operating System:** iOS 12.0 or higher
- **Application:** Pythonista 3 (available on App Store)
- **Python Version:** Python 3.7+ (included in Pythonista)

#### Dependencies
- `ui` - Pythonista's graphical interface framework
- `time` - Python standard module
- `threading` - Python standard module
- `typing` - Python type annotations
- `math` - Python standard mathematical module

### Installation and Setup

#### On iOS (Pythonista)
1. Install **Pythonista 3** from the App Store
2. Open Pythonista
3. Create a new Python file
4. Copy the code from `main.py`
5. Run the file

#### Alternative: Local Development Environment
For development and testing on computer (without graphical interface):
```bash
# Python 3.7 or higher required
python --version

# No additional dependencies installation required
# (uses only Python standard libraries)
```

**Note:** The graphical interface works completely only in Pythonista. In other Python environments, search functions can be executed, but without the UI.

## Project Structure

```
8-puzzle-ai/
├── main.py              # Main file with complete implementation
├── README.md            # This documentation file
└── .gitignore          # Git configuration
```

### Code Architecture

#### 1. Data Structures (Lines 16-104)
```python
- Stack          # Stack for DFS
- Queue          # Queue for BFS  
- MinHeap        # Min heap for informed algorithms
```

#### 2. Core Abstractions (Lines 106-160)
```python
- State          # Abstract class for states
- Problem        # Abstract class for problems
- Node           # Search tree node
```

#### 3. 8-Puzzle Implementation (Lines 162-210)
```python
- PuzzleState    # Specific puzzle state
- Puzzle         # Puzzle problem definition
```

#### 4. Heuristic Functions (Lines 212-283)
```python
- misplaced()           # Misplaced tiles heuristic
- manhattan()           # Manhattan distance heuristic
- linear_conflict()     # Linear conflict heuristic
```

#### 5. Search Algorithms (Lines 309-473)
```python
- BFS()          # Breadth-first search
- DFS()          # Depth-first search
- A_star()       # A* algorithm
- Greedy()       # Greedy search
- IDA_star()     # Iterative deepening A*
```

#### 6. Graphical Interface (Lines 476-743)
```python
- PuzzleView     # Main UI class
- setup_ui()     # Interface setup
- Event handlers # Button event handling
```

## Application Usage

### Steps to Use the App

1. **Run the application** in Pythonista
2. **Shuffle the puzzle** using the "Shuffle" button
3. **Select algorithm** (BFS, DFS, A*, Greedy, IDA*)
4. **Select heuristic** (for informed algorithms)
5. **Press "Solve"** to find the solution
6. **Use "Animate"** to see the solution step by step
7. **"Reset"** to return to goal state

### Available Controls

- **Solve:** Executes the selected algorithm
- **Shuffle:** Generates a random initial state
- **Animate:** Shows solution animation
- **Reset:** Returns to goal state (1,2,3,4,5,6,7,8,_)

### Results Interpretation

The application displays:
- **Execution time** in seconds
- **Number of expanded nodes** (complexity)
- **Solution path length**
- **Movement sequence** (UP, DOWN, LEFT, RIGHT)

## Algorithms and Complexity

### Performance Comparison

| Algorithm | Completeness | Optimality | Time Complexity | Space Complexity |
|-----------|-------------|-------------|-----------------|------------------|
| BFS       | ✅ Yes       | ✅ Yes       | O(b^d)          | O(b^d)           |
| DFS       | ❌ No        | ❌ No        | O(b^m)          | O(bm)            |
| A*        | ✅ Yes       | ✅ Yes       | O(b^d)          | O(b^d)           |
| Greedy    | ❌ No        | ❌ No        | O(b^m)          | O(b^m)           |
| IDA*      | ✅ Yes       | ✅ Yes       | O(b^d)          | O(bd)            |

*where b = branching factor, d = solution depth, m = maximum depth*

### Usage Recommendations

- **For optimal solutions:** Use A* or BFS
- **For memory efficiency:** Use IDA*
- **For quick exploration:** Use Greedy (doesn't guarantee optimization)
- **For difficult states:** Use A* with Linear Conflict heuristic

## Advanced Technical Features

### Implemented Optimizations
- **Repeated state detection** to avoid cycles
- **Admissible heuristics** to guarantee optimality
- **Non-blocking interface** using threading
- **Smooth animations** for visualization
- **Efficient memory management** with custom structures

### Implementation Details
- **Object-oriented programming** with inheritance and polymorphism
- **Type hints** for better code documentation
- **Robust exception handling**
- **Separation of responsibilities** between logic and UI

## Educational Use Cases

This application is ideal for:
- **AI students** learning search algorithms
- **Empirical comparison** of different strategies
- **Visualization** of abstract search concepts
- **Experimentation** with custom heuristics
- **Computational complexity analysis**

## Known Limitations

- **Pythonista dependency** for complete interface
- **Very complex problems** may require long computation time
- **DFS may not find solution** in some cases
- **Limited memory** on mobile devices

## Future Extensions

- Support for N×N puzzles (15-puzzle, 24-puzzle)
- More search algorithms (RBFS, SMA*)
- Additional customizable heuristics
- Competition mode between algorithms
- Results and statistics export

## Author and Academic Context

**Student:** Adrián Fernando Gaitán Londoño  
**Course:** Artificial Intelligence  
**Assignment:** AI Search Algorithms on Mobile with Python  
**Focus:** Practical implementation of search algorithms on mobile devices

---

*This project demonstrates the practical application of fundamental Artificial Intelligence concepts in an interactive mobile environment, facilitating learning and experimentation with different search strategies.*