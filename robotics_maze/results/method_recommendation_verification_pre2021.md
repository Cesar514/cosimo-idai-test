# Method Recommendation Verification — Pre-2021 Literature Justification

**Scope:** `robotics_maze/` — all planner recommendations  
**Audit date:** 2026-02-26  
**Constraint:** All supporting literature must be published in **2020 or earlier**.

---

## 1. Method Verification Matrix

| # | Recommended Method | File-path Evidence | Classification | Notes |
|---|---|---|---|---|
| 1 | A\* (A-Star) | `robotics_maze/README.md` (§1) | **Docs-only** | Described but no source code |
| 2 | Dijkstra's Algorithm | `robotics_maze/README.md` (§2) | **Docs-only** | Described but no source code |
| 3 | D\*-Lite | `robotics_maze/README.md` (§3) | **Docs-only** | Described but no source code |
| 4 | RRT | `robotics_maze/README.md` (§4) | **Docs-only** | Described but no source code |
| 5 | Wavefront / BFS Planner | `robotics_maze/README.md` (§5) | **Docs-only** | Described but no source code |
| 6 | Bug Algorithms | `robotics_maze/README.md` (§6) | **Docs-only** | Described but no source code |
| 7 | Potential Field Method | `robotics_maze/README.md` (§7) | **Docs-only** | Described but no source code |

**Classification legend**

| Label | Meaning |
|---|---|
| Implemented | Working source code exists and has tests |
| Partial | Source code started but incomplete or untested |
| Docs-only | Recommendation exists only in README/documentation |
| Missing | No mention anywhere in the repository |

**Summary:** 7 methods recommended, 7 classified as **docs-only**, 0 fully implemented.

---

## 2. Pre-2021 Literature Justification

All references below were published in 2020 or earlier and directly support the planner recommendations above.

### Ref-01 — Hart, Nilsson & Raphael (1968)
> Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A formal basis for the heuristic determination of minimum cost paths. *IEEE Transactions on Systems Science and Cybernetics*, 4(2), 100–107.  
> DOI: [10.1109/TSSC.1968.300136](https://doi.org/10.1109/TSSC.1968.300136)

**Relevance (Supports Rec. 1 — A\*):** Foundational paper introducing A\*. Proves that an admissible, consistent heuristic yields an optimal path and that A\* expands no more nodes than any other algorithm with the same heuristic. Directly validates the recommendation to use A\* as the primary planner for known static maze maps.

---

### Ref-02 — Dijkstra (1959)
> Dijkstra, E. W. (1959). A note on two problems in connexion with graphs. *Numerische Mathematik*, 1(1), 269–271.  
> DOI: [10.1007/BF01386390](https://doi.org/10.1007/BF01386390)

**Relevance (Supports Rec. 2 — Dijkstra):** Original exposition of uniform-cost search on weighted graphs. Establishes correctness and optimality guarantees that justify its use as a heuristic-free benchmark in maze environments where no distance estimate is available.

---

### Ref-03 — Stentz (1994)
> Stentz, A. (1994). Optimal and efficient path planning for partially-known environments. In *Proceedings of IEEE International Conference on Robotics and Automation (ICRA)*, 3310–3317.  
> DOI: [10.1109/ROBOT.1994.351061](https://doi.org/10.1109/ROBOT.1994.351061)

**Relevance (Supports Rec. 3 — D\*/D\*-Lite):** Introduces D\* (Dynamic A\*), the predecessor of D\*-Lite, demonstrating efficient re-planning when the environment changes during traversal. Provides the theoretical basis for incremental path repair, which Rec. 3 recommends for dynamic maze settings.

---

### Ref-04 — Koenig & Likhachev (2002)
> Koenig, S., & Likhachev, M. (2002). D\* Lite. In *Proceedings of the National Conference on Artificial Intelligence (AAAI)*, 476–483.  
> Available: <https://idm-lab.org/bib/abstracts/papers/aaai02b.pdf>

**Relevance (Supports Rec. 3 — D\*-Lite):** Presents D\*-Lite, a simpler and equally efficient formulation of the original D\* algorithm. Shows constant-factor speedups over D\* on field-robot benchmarks, making it the practical choice cited in Rec. 3 for robots that must replan as new obstacles are sensed.

---

### Ref-05 — LaValle (1998)
> LaValle, S. M. (1998). Rapidly-exploring random trees: A new tool for path planning. *Technical Report TR 98-11*, Iowa State University.  
> Available: <http://msl.cs.uiuc.edu/~lavalle/papers/Lav98c.pdf>

**Relevance (Supports Rec. 4 — RRT):** Introduces the Rapidly-exploring Random Tree (RRT). Demonstrates space-filling coverage of configuration spaces without grid discretization. Justifies the recommendation to use RRT for high-dimensional or continuous robot configuration spaces.

---

### Ref-06 — Kavraki, Švestka, Latombe & Overmars (1996)
> Kavraki, L. E., Švestka, P., Latombe, J.-C., & Overmars, M. H. (1996). Probabilistic roadmaps for path planning in high-dimensional configuration spaces. *IEEE Transactions on Robotics and Automation*, 12(4), 566–580.  
> DOI: [10.1109/70.508439](https://doi.org/10.1109/70.508439)

**Relevance (Supports Rec. 4 — RRT, broader sampling context):** Introduces Probabilistic Roadmaps (PRM), establishing the sampling-based paradigm. Empirically shows that random sampling outperforms deterministic grid discretization in complex environments, providing additional motivation for sampling-based planners as alternatives to A\*.

---

### Ref-07 — Khatib (1986)
> Khatib, O. (1986). Real-time obstacle avoidance for manipulators and mobile robots. *The International Journal of Robotics Research*, 5(1), 90–98.  
> DOI: [10.1177/027836498600500106](https://doi.org/10.1177/027836498600500106)

**Relevance (Supports Rec. 7 — Potential Field Method):** Seminal paper introducing artificial potential fields for real-time robot navigation. Defines the attractive/repulsive formulation adopted in Rec. 7 and documents its local-minima limitation, which is explicitly noted in the README.

---

### Ref-08 — Lumelsky & Stepanov (1987)
> Lumelsky, V. J., & Stepanov, A. A. (1987). Path-planning strategies for a point mobile automaton moving amidst unknown obstacles of arbitrary shape. *Algorithmica*, 2(1–4), 403–430.  
> DOI: [10.1007/BF01840369](https://doi.org/10.1007/BF01840369)

**Relevance (Supports Rec. 6 — Bug Algorithms):** Formalises Bug0 and Bug1 algorithms and proves completeness and path-length bounds. Provides the theoretical underpinning for reactive wall-following navigation recommended in Rec. 6 for sensor-constrained robots.

---

### Ref-09 — Thrun, Burgard & Fox (2005)
> Thrun, S., Burgard, W., & Fox, D. (2005). *Probabilistic Robotics*. MIT Press.  
> ISBN: 0-262-20162-3

**Relevance (Broad — all planners):** Standard graduate reference textbook in mobile robotics. Chapter 6 (Probabilistic Motion Models) and Chapter 9 (Occupancy Grid Mapping) provide the mathematical framework used by A\*, D\*-Lite, and RRT when operating on sensor-derived maps. Justifies the overall planning architecture described in this module.

---

### Ref-10 — LaValle (2006)
> LaValle, S. M. (2006). *Planning Algorithms*. Cambridge University Press.  
> Available online (open access): <http://planning.cs.uiuc.edu/>

**Relevance (Broad — Recs. 1–7):** Comprehensive open-access textbook covering A\*, Dijkstra, sampling-based planners (RRT, PRM), potential fields, and reactive navigation in a unified treatment. Directly supports every method recommended in this module.

---

### Ref-11 — Karaman & Frazzoli (2011)
> Karaman, S., & Frazzoli, E. (2011). Sampling-based algorithms for optimal motion planning. *The International Journal of Robotics Research*, 30(7), 846–894.  
> DOI: [10.1177/0278364911406761](https://doi.org/10.1177/0278364911406761)

**Relevance (Supports Rec. 4 — RRT/RRT\*):** Introduces RRT\* and PRM\*, proving asymptotic optimality of sampling-based planners. Quantifies the sub-optimality gap of vanilla RRT, motivating the selection of RRT or RRT\* based on application constraints (runtime vs. optimality). Published in 2011 — within the ≤2020 window.

---

### Ref-12 — Nash, Koenig & Tovey (2010)
> Nash, A., Koenig, S., & Tovey, C. (2010). Lazy Theta\*: Any-angle path planning and path length analysis in 3D. In *Proceedings of AAAI*, 147–154.  
> Available: <https://ojs.aaai.org/index.php/AAAI/article/view/7681>

**Relevance (Alternative to A\* — Rec. 1):** Presents Lazy Theta\* for any-angle path planning, showing shorter actual paths than grid-constrained A\* without a significant runtime penalty. Supports the note that alternatives to standard A\* should be considered for robots that are not constrained to 8-directional grid movement.

---

### Ref-13 — Pivtoraiko, Knepper & Kelly (2009)
> Pivtoraiko, M., Knepper, R. A., & Kelly, A. (2009). Differentially constrained mobile robot motion planning in state lattices. *Journal of Field Robotics*, 26(3), 308–333.  
> DOI: [10.1002/rob.20285](https://doi.org/10.1002/rob.20285)

**Relevance (Alternative to A\* — Recs. 1, 4):** Introduces state-lattice planners for kinodynamically constrained mobile robots. Demonstrates that standard A\* on a uniform grid ignores vehicle dynamics, and provides a structured sampling approach that bridges grid search and RRT-style planners.

---

## 3. Reconciliation Report

### 3.1 Valid Recommendations vs. Unsupported Claims

| Method | Supported by Pre-2021 Literature? | Repository Evidence Level | Verdict |
|---|---|---|---|
| A\* | ✅ Yes (Ref-01, Ref-10) | Docs-only | **Valid recommendation, unimplemented** |
| Dijkstra | ✅ Yes (Ref-02, Ref-10) | Docs-only | **Valid recommendation, unimplemented** |
| D\*-Lite | ✅ Yes (Ref-03, Ref-04) | Docs-only | **Valid recommendation, unimplemented** |
| RRT | ✅ Yes (Ref-05, Ref-06, Ref-11) | Docs-only | **Valid recommendation, unimplemented** |
| Wavefront/BFS | ✅ Yes (Ref-10) | Docs-only | **Valid recommendation, unimplemented** |
| Bug Algorithms | ✅ Yes (Ref-08, Ref-10) | Docs-only | **Valid recommendation, unimplemented** |
| Potential Field | ✅ Yes (Ref-07, Ref-10) | Docs-only | **Valid recommendation, unimplemented** |

**No unsupported claims detected.** All seven recommendations align with well-established, pre-2021 foundational literature.

**Key mismatch:** All methods are currently "docs-only." No algorithm has been implemented, tested, or benchmarked in this repository. The gap between recommendation and executable evidence is the primary risk.

---

### 3.2 Top 5 Remediation Steps

| Priority | Action | Rationale |
|---|---|---|
| **P1** | Implement A\* on a grid maze (`robotics_maze/planners/astar.py` or equivalent) with unit tests | A\* is the most cited recommendation and has the strongest pre-2021 backing (Ref-01). Verified code closes the docs-only gap for the primary method. |
| **P2** | Add a BFS/Wavefront planner alongside A\* as a correctness oracle | BFS provides the simplest complete planner and can be used to validate A\* results end-to-end; very low implementation cost. |
| **P3** | Implement D\*-Lite for dynamic-maze integration tests | D\*-Lite (Ref-04) is the recommended method for changing environments. Integration tests that insert obstacles mid-run would demonstrate the replanning capability. |
| **P4** | Add a benchmarking script comparing A\*, Dijkstra, BFS, and D\*-Lite on maze size / obstacle density | Converts docs-only claims into measurable evidence; enables reproducible validation of all performance claims in the README. |
| **P5** | Integrate Bug0/Bug1 reactive planner for sensor-limited experiments | Completes the reactive-navigation track (Ref-08), which is the only planner that requires no prior map and is therefore essential for field-robot scenarios discussed in the presentation slides (Slide 39–40). |

---

## 4. Acceptance-Criteria Checklist

- [x] At least 10 references from year ≤ 2020 (13 provided: Ref-01 through Ref-13; Ref-01 through Ref-10 are ≤2006; all 13 are ≤2011, well within the ≤2020 constraint)
- [x] Every recommendation checked against repository evidence (7/7 evaluated in §1 matrix)
- [x] Clear mismatch list provided (§3.1: all 7 methods are docs-only, 0 implemented)
- [x] Prioritized remediation steps provided (§3.2: P1–P5)
