# 🧩 PageRank

AI-powered implementation of the PageRank algorithm that ranks webpages by importance using both sampling (Markov Chain) and iterative methods.

## 🚀 Overview
PageRank is an algorithm for measuring the importance of web pages based on their link structure. Instead of simply counting the number of incoming links, PageRank evaluates how valuable those links are — giving higher weight to links from authoritative pages. This recursive concept enables the algorithm to distinguish between truly influential pages and those trying to game the system. In this project, two approaches are implemented to compute PageRank: one based on the behavior of a random web surfer, and another using an iterative, formula-driven method.

## 📚 PageRank Concepts
### 🧍‍♂️ Random Surfer Model
The random surfer model imagines a person navigating the web by randomly clicking links. At each step, the surfer either:

* With probability d (damping factor, typically 0.85), clicks a random link on the current page.
* With probability 1 - d, jumps to a random page from the entire corpus.

By simulating this behavior repeatedly, the frequency of visits to each page estimates its PageRank — the likelihood that a surfer lands on that page.

### 🔁 Iterative Algorithm
The iterative approach defines PageRank recursively based on the structure of the web. Starting with equal PageRank for all pages, the algorithm repeatedly applies the formula:
```
PR(p) = (1 - d) / N + d × Σ [PR(i) / NumLinks(i)]
```
Where:
* _PR(p)_ is the PageRank of page p,
* _d_ is the damping factor,
* _N_ is the total number of pages,
* _i_ ranges over all pages that link to p,
* _NumLinks(i)_ is the number of links on page i.

The iteration continues until values converge (i.e., change less than a small threshold), producing the final PageRank scores.

## 📂 Core Components
* ```crawler(corpus_dir)```: Parses HTML files into a directed link graph.
* ```transition_model(corpus, page, damping_factor)```: Computes next-page probabilities for a random surfer.
* ```sample_pagerank(corpus, damping_factor, n)```: Estimates PageRanks through random sampling.
* ```iterate_pagerank(corpus, damping_factor)```: Computes PageRanks via iterative convergence.

Example command:
```
python pagerank.py corpus0
```
Outputs sample-based and iterative PageRank values for each page
