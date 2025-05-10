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

### The modeling consist of multiple parts which help us to mathematically understand the problem we are facing, it is composed by:
- Space state: Set of all the states composing the problem
- Initial state: It is a deffinition of the starting point of our situation
- Operator/Action function: Inside a search problem, this are functions describing how the subject can move from one state to another inside the space state
- Goal state: Particular state representing the objective of the problem, it is the state we want to reach
- Path cost: Each action requires a cost to pay, the objective of the search problem is to reach the goal state from the initial state having the smallest possible cost

### Our modelation of the system

- Space state: $S = \{(i,j) | i \in [0, W-1], j \in [0, H-1], \Psi^* \le \text{Tolerance}\}$
- Initial state: \$S_0\$ = (\$i_0\$, \$j_0\$) | $\\Psi$ *  (i, j) <= Tolerance
- Goal: G = {\$p_1\$, \$p_2\$, \$p_3\$, ..., \$p_n\$} | n \$ \in \$ \$\mathbb{N}\$. \$s_goal\$ = \$p_i+1\$ = (\$i_goal\$, \$j_goal\$) \$ \in \$ S
- Operators: A(s) = {s' \in \$ S \$ | s'(i) = s(i \$\stackrel{+}{-}\$ 1) \$\lor\$ (s'(j) = s(j \$\stackrel{+}{-}\$ 1)), $\\Psi$* (s') <= Tolerance}
- Path cost: C(s, s') = $\\Psi$ *(s')

### Heuristics designed

- Euclidean distance (h1):
  Given a grid of size W x H with states composed by tuples of the form (i, j) \$ \in \$ \$\mathbb{Z}\$ ^2

  \$h_1\$ = \sqrt{(i - \$i_goal\$^2) + (j - \$j_goal\$^2)}

  and whose properties are:
    - \$h_1\$ (s) >= 0 \$ \forall s \in S \$
    - \$h_1\$ (s) = 0 if and only if s = \$s_goal\$
    - \$h_1\$ (s) <= \$h_1\$ *(s) where \$h_1\$ *(s) is the real optimum cost from s to \$s_goal\$
  - Manhattan distance (h2):
    Given a grid of size W x H with states composed by tuples of the form (i, j) \$ \in \$ \$\mathbb{Z}\$ ^2
    h(s) = |i - $i_goal\$ | + | j - $j_goal\$|

# Experiments

uwu

# Use of AI

uwu

# Conclusion

uwu
