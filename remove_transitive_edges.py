#!/usr/bin/env python

"""
    usage:
        remove_transitive_edges [options] graph.dot
    where the options are:
        -h,--help : print usage and quit

    graph.dot is a file with a directed graph. The first row is always
        
        Digraph G {

    and the last row is always 

        }

    Each row in the middle section describes an edge. For example,

        1 -> 2

    is a directed edge from a node with the label '1' to the node with the label    '2'.
"""

from sys import argv, stderr
from getopt import getopt, GetoptError
from copy import deepcopy
from graph import *

def simplify(G):
    """Simplify the graph S by removing the transitively-inferrible edges.

    S is just a copy of G, which is the input to the graph. 
    """

    S = deepcopy(G)

    changed = True
    while changed:
        changed = False
        edges_to_remove = []

        for n1 in list(S.nodes()):
            for n2 in list(S.edges[n1].keys()):
                # check if there is an alternative path from n1 to n2 (does not use direct edge)
                if has_alternative_path(S, n1, n2):
                    edges_to_remove.append((n1, n2))

        for n1, n2 in edges_to_remove:
            # check if edge has been removed before
            if S.has_edge(n1, n2):
                if has_alternative_path(S, n1, n2):
                    S.delete_edge(n1, n2)
                    changed = True

    return S

def has_alternative_path(G, src, dst):
    """
    Return True if there is a path from src to dst that does not use the direct edge
    between src and dst.
    """
    visited = set()
    stack = []

    # want paths of length >= 2
    for neighbor in G.edges[src]:
        if neighbor != dst:
            stack.append(neighbor)
        else: # src -> other node -> dst
            pass

    visited.add(src)

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == dst:
            return True
        for neighbor in G.edges.get(node, {}):
                if neighbor not in visited:
                    stack.append(neighbor)

    return False

def main(filename):
    # read the graph from the input file
    graph = Graph(filename)
    print(f"Read the graph from {filename}", file=stderr)

    # simplify the graph by removing the transitively-inferrible edges
    simplified = simplify(graph)
    print(f"Simplified the graph", file=stderr)

    # print the simplified graph in the same format as the input file
    print(simplified)

if __name__ == "__main__":
    try:
        opts, args = getopt(argv[1:], "h", ["help"])
    except GetoptError as err:
        print(err)
        print(__doc__, file=stderr)
        exit(1) 

    for o, a in opts:
        if o in ("-h", "--help"):
            print(__doc__, file=stderr)
            exit()
        else:
            assert False, "unhandled option"

    if len(args) != 1:
        print(__doc__, file=stderr)
        exit(2)

    main(args[0])
