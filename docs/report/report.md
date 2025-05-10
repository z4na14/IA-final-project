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

$$s_{goal} = \left\{(y_i,x_i) \right\}_{i=1}^k \text{ where each } p_i \mapsto (y_i,x_i)$$

#### Solution Characteristics:

A solution is a path $\pi = [s_0, s_1, \text{ ...}, s_n]$ where:

1. $s_n \in s_goal$
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



# Experiments

uwu

# Use of AI

uwu

# Conclusion

uwu
