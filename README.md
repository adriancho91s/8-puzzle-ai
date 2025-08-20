# Buscadores IA en Móvil con Python - 8-Puzzle

**Taller de Inteligencia Artificial - Implementación de Algoritmos de Búsqueda**

**Autor:** Adrián Fernando Gaitán Londoño

## Descripción del Proyecto

Este proyecto implementa una aplicación móvil interactiva para resolver el clásico problema del 8-puzzle utilizando diferentes algoritmos de búsqueda de Inteligencia Artificial. La aplicación está desarrollada en Python usando el framework Pythonista para dispositivos iOS, proporcionando una interfaz gráfica intuitiva para experimentar con diversos algoritmos de búsqueda.

## Características Principales

### Algoritmos de Búsqueda Implementados
- **BFS (Breadth-First Search)** - Búsqueda en Amplitud
- **DFS (Depth-First Search)** - Búsqueda en Profundidad
- **A*** - Algoritmo A Estrella
- **Greedy** - Búsqueda Voraz
- **IDA*** - A* con Profundización Iterativa

### Funciones Heurísticas
- **Manhattan Distance** - Distancia Manhattan
- **Misplaced Tiles** - Fichas Fuera de Lugar
- **Linear Conflict** - Conflicto Lineal (Heurística Avanzada)

### Funcionalidades de la Aplicación
- Interfaz gráfica interactiva con grid 3x3
- Selección de algoritmos y heurísticas
- Animación paso a paso de la solución
- Mezcla aleatoria del puzzle
- Estadísticas de rendimiento (nodos expandidos, tiempo de ejecución)
- Visualización del camino de la solución

## Entorno de Ejecución

### Requisitos del Sistema

#### Plataforma Principal: iOS con Pythonista
- **Sistema Operativo:** iOS 12.0 o superior
- **Aplicación:** Pythonista 3 (disponible en App Store)
- **Versión de Python:** Python 3.7+ (incluido en Pythonista)

#### Dependencias
- `ui` - Framework de interfaz gráfica de Pythonista
- `time` - Módulo estándar de Python
- `threading` - Módulo estándar de Python
- `typing` - Anotaciones de tipo de Python
- `math` - Módulo matemático estándar

### Instalación y Configuración

#### En iOS (Pythonista)
1. Instalar **Pythonista 3** desde el App Store
2. Abrir Pythonista
3. Crear un nuevo archivo Python
4. Copiar el código de `main.py`
5. Ejecutar el archivo

#### Alternativa: Entorno de Desarrollo Local
Para desarrollo y testing en computadora (sin interfaz gráfica):
```bash
# Python 3.7 o superior requerido
python --version

# No requiere instalación de dependencias adicionales
# (usa solo bibliotecas estándar de Python)
```

**Nota:** La interfaz gráfica solo funciona completamente en Pythonista. En otros entornos Python, las funciones de búsqueda pueden ejecutarse, pero sin la UI.

## Estructura del Proyecto

```
8-puzzle-ai/
├── main.py              # Archivo principal con toda la implementación
├── README.md            # Este archivo de documentación
└── .gitignore          # Configuración de Git
```

### Arquitectura del Código

#### 1. Estructuras de Datos (Líneas 16-85)
```python
- Stack          # Pila para DFS
- Queue          # Cola para BFS  
- MinHeap        # Heap mínimo para algoritmos informados
```

#### 2. Abstracciones Centrales (Líneas 86-160)
```python
- State          # Clase abstracta para estados
- Problem        # Clase abstracta para problemas
- Node           # Nodo del árbol de búsqueda
```

#### 3. Implementación del 8-Puzzle (Líneas 161-210)
```python
- PuzzleState    # Estado específico del puzzle
- Puzzle         # Definición del problema del puzzle
```

#### 4. Funciones Heurísticas (Líneas 211-260)
```python
- misplaced()           # Heurística de fichas mal ubicadas
- manhattan()           # Heurística de distancia Manhattan
- linear_conflict()     # Heurística de conflicto lineal
```

#### 5. Algoritmos de Búsqueda (Líneas 280-420)
```python
- BFS()          # Búsqueda en amplitud
- DFS()          # Búsqueda en profundidad
- A_star()       # Algoritmo A*
- Greedy()       # Búsqueda voraz
- IDA_star()     # A* con profundización iterativa
```

#### 6. Interfaz Gráfica (Líneas 430-742)
```python
- PuzzleView     # Clase principal de la UI
- setup_ui()     # Configuración de la interfaz
- Event handlers # Manejo de eventos de botones
```

## Uso de la Aplicación

### Pasos para Usar la App

1. **Ejecutar la aplicación** en Pythonista
2. **Mezclar el puzzle** usando el botón "Mezclar"
3. **Seleccionar algoritmo** (BFS, DFS, A*, Greedy, IDA*)
4. **Seleccionar heurística** (para algoritmos informados)
5. **Presionar "Resolver"** para encontrar la solución
6. **Usar "Animar"** para ver la solución paso a paso
7. **"Reset"** para volver al estado objetivo

### Controles Disponibles

- **Resolver:** Ejecuta el algoritmo seleccionado
- **Mezclar:** Genera un estado inicial aleatorio
- **Animar:** Muestra la animación de la solución
- **Reset:** Regresa al estado objetivo (1,2,3,4,5,6,7,8,_)

### Interpretación de Resultados

La aplicación muestra:
- **Tiempo de ejecución** en segundos
- **Número de nodos expandidos** (complejidad)
- **Longitud del camino** de la solución
- **Secuencia de movimientos** (UP, DOWN, LEFT, RIGHT)

## Algoritmos y Complejidad

### Comparación de Rendimiento

| Algoritmo | Completitud | Optimalidad | Complejidad Temporal | Complejidad Espacial |
|-----------|-------------|-------------|---------------------|---------------------|
| BFS       | ✅ Sí       | ✅ Sí       | O(b^d)              | O(b^d)              |
| DFS       | ❌ No       | ❌ No       | O(b^m)              | O(bm)               |
| A*        | ✅ Sí       | ✅ Sí       | O(b^d)              | O(b^d)              |
| Greedy    | ❌ No       | ❌ No       | O(b^m)              | O(b^m)              |
| IDA*      | ✅ Sí       | ✅ Sí       | O(b^d)              | O(bd)               |

*donde b = factor de ramificación, d = profundidad de la solución, m = profundidad máxima*

### Recomendaciones de Uso

- **Para soluciones óptimas:** Usar A* o BFS
- **Para eficiencia de memoria:** Usar IDA*
- **Para exploración rápida:** Usar Greedy (no garantiza optimización)
- **Para estados difíciles:** Usar A* con heurística Linear Conflict

## Características Técnicas Avanzadas

### Optimizaciones Implementadas
- **Detección de estados repetidos** para evitar ciclos
- **Heurísticas admisibles** para garantizar optimalidad
- **Interfaz no bloqueante** usando threading
- **Animaciones suaves** para visualización
- **Manejo eficiente de memoria** con estructuras personalizadas

### Detalles de Implementación
- **Programación orientada a objetos** con herencia y polimorfismo
- **Type hints** para mejor documentación del código
- **Manejo de excepciones** robusto
- **Separación de responsabilidades** entre lógica y UI

## Casos de Uso Educativos

Esta aplicación es ideal para:
- **Estudiantes de IA** que aprenden algoritmos de búsqueda
- **Comparación empírica** de diferentes estrategias
- **Visualización** de conceptos abstractos de búsqueda
- **Experimentación** con heurísticas personalizadas
- **Análisis de complejidad** computacional

## Limitaciones Conocidas

- **Dependencia de Pythonista** para la interfaz completa
- **Problemas muy complejos** pueden requerir mucho tiempo de cómputo
- **DFS puede no encontrar solución** en algunos casos
- **Memoria limitada** en dispositivos móviles

## Extensiones Futuras

- Soporte para puzzles N×N (15-puzzle, 24-puzzle)
- Más algoritmos de búsqueda (RBFS, SMA*)
- Heurísticas adicionales personalizables
- Modo de competencia entre algoritmos
- Exportación de resultados y estadísticas

## Autor y Contexto Académico

**Estudiante:** Adrián Fernando Gaitán Londoño  
**Materia:** Inteligencia Artificial  
**Taller:** Buscadores IA en Móvil con Python  
**Enfoque:** Implementación práctica de algoritmos de búsqueda en dispositivos móviles

---

*Este proyecto demuestra la aplicación práctica de conceptos fundamentales de Inteligencia Artificial en un entorno móvil interactivo, facilitando el aprendizaje y la experimentación con diferentes estrategias de búsqueda.*