---
grado: Bachelor in Computer Science and Engineering
asignatura: Artificial Intelligence
anio-academico: 2024-2025
grupo: 89
autores:
  - nombre: Jorge Adrian Saghin Dudulea
    nia: 100522257
  - nombre: Denis Loren Moldovan
    nia: 100522240
  - nombre: Ignacio Cortina de Antonio
    nia: 100522372
nombre-lab: Final practice
titulo: Heuristic Search in Radars
---

# Introduction

uwu

# Explanation of the system

uwu

## Mathematical modeling of the search problem

#### State Space: 
Let the state space $S$ be defined as:

$$S = \{(y,x) \in \mathbb{Z}^2 | 0 \leq y < H, 0 \leq x < W, \Psi^*(y,x) \leq \tau\}$$

where:
  - $H \times W$: Dimensions of the grid
  - $\Psi^*: \mathbb{Z}^2 \rightarrow [\epsilon,1]$: Scaled detection probability function
  - $\tau \in (0,1]$: Detection tolerance threshold

#### Operator Set:

The action set $A$ defines valid transitions between states:
$$A=\{Up, Down, Left, Right\}$$

Each action $a \in A$ maps to a movement vector:

$$
\delta(a)=
\begin{cases}
(-1,0) & \text{if } a = Up \\
(1,0) & \text{if } a = Down \\
(0,-1) & \text{if } a = Left \\
(0,1) & \text{if } a = Right
\end{cases}
$$

#### Transaction Function:

$$T:S \times A \rightarrow \text{S }\cup \{\emptyset\}$$
$$
T((y,x),a) = 
\begin{cases}
(y',x') & \text{if }(y',x') \in S\text{ where } (y',x') = (y,x) + \delta(a) \\
\emptyset & \text{otherwise}
\end{cases}
$$

#### Cost function:
$$c((y_1,x_1),(y_2,x_2) = \Psi^* (y_2,x_2)$$

## Initial and Goal States

#### Initial State:
$$s_0 = (y_0, x_0) \text{ where }(lat_0, lon_0) \mapsto (y_0,x_0)$$

#### Goal State:

For a sequence of POIs $\{p_1,\text{ ...},p_k\}$:

$$s_{goal} = \{(y_i,x_i)\}_{i=1}^k \text{ where each } p_i \mapsto (y_i,x_i)$$

#### Solution Characteristics:

A solution is a path $\pi = [s_0, s_1, \text{ ...}, s_n]$ where:

1. $s_n \in s_{goal}$
2. $\forall i, \exists a \in A \text{ such that } s_{i+1} = T(s_i, a)$
3. Total costs $C(\pi) = \sum_{i = 0}^{n-1} c(s_i, s_{i + 1})$ is minimized

## Heuristics designed

### Euclidean distance:
  
$$h_1((y,x),(y_{goal},x_{goal})) = \sqrt{(y - y_{goal})^2 + (x - x_{goal})^2} \cdot \epsilon$$

#### Admissibility Proof:
1. Actual path cost between adjacent cells $\geq \epsilon$
2. Straight-line distance is the minimum possible path length
3. Thus $h_1 \leq$ actual cost (underestimates)

### Manhattan distance:
  
$$h_2((y, x), (y_{goal}, x_{goal})) = (|y - y_{goal}| + |x - x_{goal}|) \cdot \epsilon$$

#### Admissibility Proof:
1. Manhattan distance $\geq$ Euclidean distance
2. Each move costs $\geq \epsilon$
3. Therefore $h_2 \leq$ actual cost (underestimates)

## Map and searh space generation

### Implementation of the map
Let the rectangular area delimited by geodetic coordinates (lat_0 ,long_0) (lat_1, long_1) be devided into a grid H x W. Each cell represents a unique point in where
- The latitude and longitude intervals are calculated as

$$
\Delta\ lat = \frac{lat_0-lat_1}{H-1}
\Delta\ long = \frac{long_0-long_1}{W-1}
$$
- Each cell (i, j) is mapped to a geographic coordinates:  
$$
lat_i = lat_1 + i· \Delta lat, lon_j = long_0 + j · \Delta lon
$$

For each radar $r_k \in \{1, 2, ..., N_r\}$, located in the coordinates $(lat_k, lon_k)$, we compute:

- The maximum detection range ($R_{max}$) using the provided rada equation.  
$$
 R_{max} = \frac{P_t G^2 \lambda \sigma}{(4 \pi)^3 P_{min} L}$
$$
- The euclidean distance ($d$) from each grid cell to the radar using the conversion factor $K = 111.000$ (meters per degree)
$$
d = K·\sqrt{(lat_i-lat_k)^2+(lon_1-lon_k)^2}
$$
-  If $d \leq R$, compute the detection possibility using the 2D Gaussian function
$$
\Psi_k^*(i,j) = \frac{e^{-\frac{1}{2}(x - \mu)^T \Sigma^{-1}(x - \mu)}}{(2\pi)^\frac{n}{2} |\Sigma|^\frac{1}{2}}
$$
  Where 
   - $x = (lat_i, lon_j)$
   - $\mu = (lat_k, lon_k)$
   - $\Sigma$ is the covariance matrix, typically diagonal (can be fixed for simplification)
- if $d > R_{max}$, set $\Psi^*_k(i,j) = 0$
- Then for each cell, compute the maximum detection possibility from all radars:
$$
\Psi^*(i,j) = max_k \Psi^*_k(i,j)
$$

The raw detection possibilities $\Psi^*(i,j)$ are scaled to the interval $[\epsilon, 1]$ using the modified Min-Max normalization:

$$
\Psi^*_{\text{scaled}}(i,j) = \left( \frac{\Psi^*(i,j) - \Psi^*_{\min}}{\Psi^*_{\max} - \Psi^*_{\min}} \right) \cdot (1 - \epsilon) + \epsilon
$$

where:
- $\Psi_{\min}$ and $\Psi_{\max}$ are the minimum and maximum non-zero detection values in the map.
- $\epsilon$ is a small positive constant to ensure no cell has cost 0 (e.g., $\epsilon = 0.001$)

The resulting detection map is stored in memory as a matrix:

$$
M \in \mathbb{R}^{H \times W}, \quad M[i][j] = \Psi^*_{\text{scaled}}(i,j)
$$

## Search graph generation

Given the detection map $M$, we construct a directed weighted graph $G = (V, E)$, where:

### 2.1 Vertices

Each vertex $v_{i,j} \in V$ corresponds to a cell $(i,j)$ such that:

$$
M[i][j] \leq \text{detection threshold}
$$

Only these vertices are considered traversable by the spy plane.

### 2.2 Edges

An edge exists between vertex $v_{i,j}$ and its valid neighbors $v_{i',j'}$ if:

$$
(i', j') \in \{(i+1, j), (i-1, j), (i, j+1), (i, j-1)\}
$$

and both cells satisfy:

$$
M[i][j] \leq \text{threshold}, \quad M[i'][j'] \leq \text{threshold}
$$

For each such edge:

$$
e_{(i,j) \rightarrow (i',j')} \in E \quad \text{with weight} \quad w = M[i'][j']
$$

That is, the cost of moving from a cell to a neighbor is the detection cost of the **destination** cell, reflecting the risk of exposure.

The graph is stored in memory as an adjacency list or adjacency matrix, depending on the implementation.


# Experiments

uwu

# Use of AI

uwu

# Conclusion

uwu
