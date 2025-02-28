# src/algorithms.py

import heapq
from collections import deque

def bfs(graph, start, goal):
    """
    Breadth-First Search (BFS) for finding the shortest path in an unweighted graph.

    Parameters:
        graph: a networkx graph
        start: starting word (node)
        goal: target word (node)
        
    Returns:
        A list of words representing the shortest path from start to goal, or None if no path exists.
    """
    # Using a deque as our queue; each element is a tuple (current_node, path_so_far)
    queue = deque()
    queue.append((start, [start]))
    visited = {start}
    
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
        
        # Iterate over all neighboring words (nodes)
        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None  # Return None if no path is found

def ucs(graph, start, goal):
    """
    Uniform Cost Search (UCS) for finding the shortest path in a graph with uniform edge costs.
    In this word ladder, every edge has a cost of 1, so UCS behaves similarly to BFS.

    Parameters:
        graph: a networkx graph
        start: starting word (node)
        goal: target word (node)
        
    Returns:
        A list of words representing the path from start to goal, or None if no path exists.
    """
    # Priority queue stores tuples: (accumulated_cost, current_node, path_so_far)
    pq = []
    heapq.heappush(pq, (0, start, [start]))
    visited = {}  # Tracks the lowest cost at which we've seen each node

    while pq:
        cost, current, path = heapq.heappop(pq)
        if current == goal:
            return path
        
        # If we've reached the node with a lower cost before, skip this one.
        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        
        for neighbor in graph.neighbors(current):
            new_cost = cost + 1  # Each move costs 1
            heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))
    return None

def heuristic(word, goal):
    """
    Heuristic function for A* Search: counts how many letters differ between the current word and the goal.
    This is admissible because each differing letter requires at least one transformation.

    Parameters:
        word: the current word
        goal: the target word

    Returns:
        An integer representing the estimated number of moves to reach the goal.
    """
    return sum(1 for a, b in zip(word, goal) if a != b)

def astar(graph, start, goal):
    """
    A* Search algorithm that combines the actual cost and a heuristic estimate to find the optimal path.

    Parameters:
        graph: a networkx graph
        start: starting word (node)
        goal: target word (node)
        
    Returns:
        A list of words representing the optimal path from start to goal, or None if no path exists.
    """
    # Priority queue stores tuples: (f, cost, current_node, path_so_far)
    # f = cost so far + heuristic estimate
    pq = []
    start_h = heuristic(start, goal)
    heapq.heappush(pq, (start_h, 0, start, [start]))
    visited = {}  # Records the lowest cost at which we reached each node

    while pq:
        f, cost, current, path = heapq.heappop(pq)
        if current == goal:
            return path
        
        if current in visited and visited[current] <= cost:
            continue
        visited[current] = cost
        
        for neighbor in graph.neighbors(current):
            new_cost = cost + 1  # Uniform cost for each transformation
            new_f = new_cost + heuristic(neighbor, goal)
            heapq.heappush(pq, (new_f, new_cost, neighbor, path + [neighbor]))
    return None

def search_path(graph, start, goal, algorithm="bfs"):
    """
    Utility function to choose the search algorithm based on a string parameter.

    Parameters:
        graph: a networkx graph
        start: starting word (node)
        goal: target word (node)
        algorithm: one of "bfs", "ucs", or "astar"

    Returns:
        A list of words representing the path, or None if no path is found.
    """
    algorithm = algorithm.lower()
    if algorithm == "bfs":
        return bfs(graph, start, goal)
    elif algorithm == "ucs":
        return ucs(graph, start, goal)
    elif algorithm == "astar":
        return astar(graph, start, goal)
    else:
        raise ValueError("Unknown algorithm. Please choose from 'bfs', 'ucs', or 'astar'.")

if __name__ == "__main__":
    # For demonstration: create a simple graph of words of the same length.
    import networkx as nx

    # Example words (ensure they are all the same length for a valid word ladder)
    words = ["cat", "bat", "bet", "bed", "bad", "cad"]
    
    # Build a simple graph manually for words of length 3.
    G = nx.Graph()
    G.add_nodes_from(words)
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            # Check if the words differ by exactly one letter.
            if sum(1 for a, b in zip(words[i], words[j]) if a != b) == 1:
                G.add_edge(words[i], words[j])
    
    start_word = "cat"
    goal_word = "bed"
    
    print("BFS path:", bfs(G, start_word, goal_word))
    print("UCS path:", ucs(G, start_word, goal_word))
    print("A* path:", astar(G, start_word, goal_word))
