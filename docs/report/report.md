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
nombre-lab: Artificial Intelligence Practice
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

# Experiments

uwu

# Use of AI

uwu

# Conclusion

uwu
