import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probability_distribution = {}
    linked_pages = corpus[page]
    num_pages = len(corpus)

    if linked_pages:
        # Damping factor applied to linked pages
        for p in corpus:
            probability_distribution[p] = (1 - damping_factor) / num_pages
            if p in linked_pages:
                probability_distribution[p] += damping_factor / len(linked_pages)
    else:
        # No links, distribute evenly to all pages
        for p in corpus:
            probability_distribution[p] = 1 / num_pages

    return probability_distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    
    # Start with a random page
    current_page = random.choice(pages)

    for _ in range(n):
        page_rank[current_page] += 1
        # Get transition model for the current page
        model = transition_model(corpus, current_page, damping_factor)
        # Choose next page based on transition model probabilities
        current_page = random.choices(list(model.keys()), weights=model.values(), k=1)[0]

    # Normalize to make it sum to 1
    total_samples = sum(page_rank.values())
    for page in page_rank:
        page_rank[page] /= total_samples

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pagerank = {page: 1 / num_pages for page in corpus}
    new_pagerank = pagerank.copy()

    # Repeat until values converge
    converged = False
    while not converged:
        converged = True
        for page in corpus:
            # Calculate the new PageRank for `page`
            rank = (1 - damping_factor) / num_pages
            for potential_link in corpus:
                if page in corpus[potential_link]:
                    rank += damping_factor * \
                        (pagerank[potential_link] / len(corpus[potential_link]))
                elif not corpus[potential_link]:  # If a page has no links
                    rank += damping_factor * (pagerank[potential_link] / num_pages)

            # Check for convergence
            if abs(new_pagerank[page] - rank) > 0.001:
                converged = False
            new_pagerank[page] = rank

        pagerank = new_pagerank.copy()

    # Normalize the values
    total_rank = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= total_rank

    return pagerank


if __name__ == "__main__":
    main()
