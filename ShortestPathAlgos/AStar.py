


"""
    A* algorithm som beskrevet i bogen:
    A classic goal-directed shortest path algorithm is A* search. It
    uses a potential function π : V → R on the vertices, which is a lower bound on
    the distance dist(u, t) from u to t. It then runs a modified version of Dijkstra’s
    algorithm in which the priority of a vertex u is set to dist(s, u) + π(u). This
    causes vertices that are closer to the target t to be scanned earlier during the
    algorithm.

"""

def AStar(graph, source, target):
    return