# R8 Research: Fringe Search for Faster A*-Like Planning

## Core Idea
Fringe Search (Bjornsson et al., 2005) is a heuristic graph search method in the A* family:
- It still evaluates `f(n) = g(n) + h(n)`.
- It avoids a global priority queue for every expansion.
- It processes nodes in thresholded passes using two lists:
  - `now`: nodes with `f <= current_threshold`
  - `later`: nodes deferred to a higher threshold

At the end of each pass, threshold increases to the smallest deferred `f`, and search continues.

## Why It Can Be Faster Than Standard A*
On many grid maps, large groups of frontier nodes have very similar `f` values.
For that regime, Fringe Search can outperform A* because it:
- reduces heap `push/pop` traffic (fewer `O(log n)` queue operations),
- improves locality with simple list scans/appends,
- batches work by threshold instead of strict global ordering at every step.

Asymptotically, both are still worst-case exponential in hard mazes, but practical constant factors can favor Fringe Search.

## Where It Typically Outperforms A*
Fringe Search is a strong candidate when:
- edge costs are uniform (unit-cost grid moves),
- heuristic is admissible/consistent but not sharply discriminative,
- many nodes share near-identical priorities (wide open areas, long frontiers),
- benchmark objective is wall-clock speed over strict node ordering overhead.

In these settings, path quality remains optimal with consistent heuristics, while runtime can improve due to lower queue overhead.

## Where A* Can Still Win
- Highly informative heuristics that keep A* frontier very small.
- Problems where strict best-first ordering significantly prunes expansions early.
- Implementations that rely on advanced PQ optimizations or additional pruning not used in Fringe Search.

## Practical Use in This Project
For the robotics maze benchmark:
- Treat Fringe Search as an A*-compatible baseline emphasizing throughput.
- Compare on large mazes with uniform movement cost and repeated trials.
- Track runtime + expansions together, because speedups may come mostly from lower data-structure overhead rather than fewer expansions.
