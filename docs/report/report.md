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

## Modeling of the search problem

The modeling consist of multiple parts which help us to mathematically understand the problem we are facing, it is composed by:

- Space state: Set of all the states composing the problem
$$
S = \{(i,j) | i \in [0, W-1], j \in [0, H-1], \Psi^* <= \text{Tolerance}\}
$$
- Initial state: It is a definition of the starting point of our situation
$$
S_0 = \{(i_0, j_0) | \Psi^*  (i, j) <= \text{Tolerance}\}
$$
- Operator/Action function: Inside a search problem, these are functions describing how the subject can move from one state to another inside the space state
$$
  A(s) = \{s' \in  S  |(s'(i) = s(i \pm 1)) \lor (s'(j) = s(j \pm 1)), \Psi^*(s') <= \text{Tolerance}\}
$$
- Goal state: Particular state representing the objective of the problem, it is the state we want to reach
$$
G = \{\{p_1, p_2, p_3, ..., p_n\} | n  \in  \mathbb{N}, s_{\text{goal}} = p_{i+1} = (i_{\text{goal}}, j_{\text{goal}})  \in  S\}
$$
- Path cost: Each action requires a cost to pay, the objective of the search problem is to reach the goal state from the initial state having the smallest possible cost
$$
C(s, s') = \Psi^*(s')
$$


### Heuristics designed

- Euclidean distance $(h_1)$:
  
  Given a grid of size $W \times H$ with states composed by tuples of the form $(i, j)  \in  \mathbb{Z}^2$

  $$h_1 = \sqrt{(i - i_{\text{goal}})^2 + (j - j_{\text{goal}})^2}$$

  And whose properties are:
    - $h_1 (s) \geq 0,  \forall s \in S$
    - $h_1 (s) = 0 \text{ iff } s = s_{\text{goal}}$
    - $h_1 (s) \leq h_1^*(s)$ where $h_1^*(s)$ is the real optimum cost from $s$ to $s_{\text{goal}}$

&nbsp;

- Manhattan distance $(h_2)$:
  
  Given a grid of size $W \times H$ with states composed by tuples of the form $(i, j)  \in  \mathbb{Z}^2$
  
  $$h(s) = |i - i_{\text{goal}} | + | j - j_{\text{goal}}|$$
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
