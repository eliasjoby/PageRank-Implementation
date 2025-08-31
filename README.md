# PageRank-Implementation
Implementing basic Page Rank Algorithm used in Search-Engine Optimization


## Overview

This project provides a Python framework to **create and analyze directed and undirected graphs** with node and edge attributes. A key feature is the **PageRank algorithm**, which ranks nodes based on their connectivity, making it ideal for search engines, network analysis, and recommendation systems.

The focus is on **understanding and applying PageRank**, highlighting its algorithmic significance rather than low-level graph implementation details.

## Features

* Create **Directed and Undirected Graphs** with arbitrary node and edge attributes.
* Load graphs directly from **CSV files**:

  * `characters-nodes.csv` – node identifiers and attributes
  * `characters-edges.csv` – edges and optional weights or labels
* **PageRank computation**:

  * Configurable **number of iterations**
  * Adjustable **damping factor** `d` (probability of continuing a random walk)
  * Handles **dangling nodes** (nodes with no outgoing edges) by redistributing their rank evenly
* Access:

  * Node degrees (`in_degree`, `out_degree`, `degree`)
  * Node and edge lookup
  * Node and edge listing
* Utility to **print ranked nodes** in a readable format

## PageRank Algorithm

PageRank assigns a score to each node based on the structure of the incoming links. Mathematically, the PageRank $PR(u)$ of a node $u$ is defined as:

$$
PR(u) = \frac{1 - d}{N} + d \sum_{v \in B_u} \frac{PR(v)}{L(v)}
$$

Where:

* `d` is the damping factor (usually 0.85)
* `N` is the total number of nodes
* `B_u` is the set of nodes linking to `u`
* `L(v)` is the out-degree of node `v`
* Dangling nodes contribute their rank evenly across all nodes

The algorithm iteratively updates ranks until convergence or a fixed number of iterations.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/distributed-search-engine.git
   cd distributed-search-engine
   ```
2. Ensure Python 3.8+ is installed.
3. No external packages are required.

## Usage

### Compute PageRank from CSV:

```python
from pagerank import pagerank_from_csv

# Compute PageRank on a directed graph
pagerank_from_csv('data/characters-nodes.csv', 'data/characters-edges.csv', num_iterations=40)
```

### Compute PageRank on an existing graph:

```python
import graph
from pagerank import pagerank, print_ranks

g = graph.DirectedGraph()
g.add_node(0, name='A')
g.add_node(1, name='B')
g.add_node(2, name='C')

g.add_edge(0, 1)
g.add_edge(1, 2)
g.add_edge(2, 0)

ranks = pagerank(g, num_iterations=50)
print_ranks(ranks)
```

### Example Output:

```
0: 0.33333
1: 0.33333
2: 0.33333
Sum: 1.00000
```

## Testing

Comprehensive tests included for:

* Single-node graphs
* Two-node cycles
* Symmetric triangles
* Graphs with dangling nodes

Run tests:

```bash
python pagerank_test.py
```

## Notes

* PageRank values **always sum to 1**.
* Dangling nodes distribute rank evenly.
* Algorithm converges with sufficient iterations.

## CSV Format

**Nodes file:**

```
id,attribute1,attribute2,...
0,nameA,cityX
1,nameB,cityY
```

**Edges file:**

```
source,target,weight
0,1,1
1,2,2
```
