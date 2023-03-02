import sys
from collections import deque

from utils import *
import SimpleProblemSolvingAgent as SPSA

#Graph Class supplied from search.py
class Graph:
    """A graph connects nodes (vertices) by edges (links). Each edge can also
    have a length associated with it. The constructor call is something like:
        g = Graph({'A': {'B': 1, 'C': 2})
    this makes a graph with 3 nodes, A, B, and C, with an edge of length 1 from
    A to B,  and an edge of length 2 from A to C. You can also do:
        g = Graph({'A': {'B': 1, 'C': 2}, directed=False)
    This makes an undirected graph, so inverse links are also added. The graph
    stays undirected; if you add more links with g.connect('B', 'C', 3), then
    inverse link is also added. You can use g.nodes() to get a list of nodes,
    g.get('A') to get a dict of links out of A, and g.get('A', 'B') to get the
    length of the link from A to B. 'Lengths' can actually be any object at
    all, and nodes can be any hashable object."""

    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        """Make a digraph into an undirected graph by adding symmetric edges."""
        for a in list(self.graph_dict.keys()):
            for (b, dist) in self.graph_dict[a].items():
                self.connect1(b, a, dist)

    def connect(self, A, B, distance=1):
        """Add a link from A and B of given distance, and also add the inverse
        link if the graph is undirected."""
        self.connect1(A, B, distance)
        if not self.directed:
            self.connect1(B, A, distance)

    def connect1(self, A, B, distance):
        """Add a link from A to B of given distance, in one direction only."""
        self.graph_dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        """Return a link distance or a dict of {node: distance} entries.
        .get(a,b) returns the distance or None;
        .get(a) returns a dict of {node: distance} entries, possibly {}."""
        links = self.graph_dict.setdefault(a, {})
        if b is None:
            return links
        else:
            return links.get(b)

    def nodes(self):
        """Return a list of nodes in the graph."""
        s1 = set([k for k in self.graph_dict.keys()])
        s2 = set([k2 for v in self.graph_dict.values() for k2, v2 in v.items()])
        nodes = s1.union(s2)
        return list(nodes)

#UndirectedGraph function supplied from search.py
def UndirectedGraph(graph_dict=None):
    """Build a Graph where every edge (including future ones) goes both ways."""
    return Graph(graph_dict=graph_dict, directed=False)

#Checks if entered cities are contained in the Romania map.
#Checks if entered cities are the same.
def checkCities(cOne, cTwo, rmap):
    cities = list(map(lambda x:x, rmap.nodes()))
    if cOne == cTwo or cOne not in cities or cTwo not in cities:
        return True
    else:
        return False

#Helper function used to test user input.
def inputTest(test):
    while test.lower() != 'yes' and test.lower() != 'no':
        test = input('Please enter yes/no (or exit to quit): ')
        if test.lower() == 'exit':
            print("Thank You for Using Our App")
            return
    return test

#Helper function used to read in the map file.
def readMap(filename):
    map = {}
    mapDone = False;
    f = open(filename, 'r')
    for line in f:
        aList = line.split(';')
        #'locations' is the keyword split between the map info and map.locations
        if aList[0] == 'locations':
            finished_map = UndirectedGraph(map)
            finished_map.locations = {}
            mapDone = True
        #if the map info is not complete, load the .csv line into the map dictionary
        if not mapDone and len(aList) > 1:
            for i in range(0, len(aList)):
                aList[i] = aList[i].rstrip('\n')
                if i == 0:
                     map[aList[i]] = {}
                elif (i % 2 == 0):
                    map[aList[0]][aList[i-1]] = int(aList[i])
        # if the map info is complete, load the .csv line into the map.locations dictionary
        elif aList[0] != 'locations':
            finished_map.locations[aList[0]] = (int(aList[1]), int(aList[2]))
    f.close()
    return finished_map

# Helper function used to call Greedy Best First Search.
# Takes in a Graph Problem and solves with Best First Search using problem.h as the heuristic.
def do_gbfs(problem):
    search_result = SPSA.best_first_graph_search(problem, problem.h)
    path = search_result.path()
    print("Using the Greedy Best First Search Method")
    print("The total cost of the path was " + str(path[-1].path_cost))
    print("The path was " + path[0].state, end=" ")
    for i in range(1, len(path)):
        print("to " + path[i].state, end=" ")
    print("\n")

# Helper function used to call A Star search method.
# Takes in a Graph Problem and solves with astar using problem.h and path cost as the heuristic.
def do_astar(problem):
    search_result = SPSA.astar_search(problem)
    path = search_result.path()
    print("Using the A Star Search Method")
    print("The total cost of the path was " + str(path[-1].path_cost))
    print("The path was " + path[0].state, end=" ")
    for i in range(1, len(path)):
        print("to " + path[i].state, end=" ")
    print("\n")

# Helper function used to call Hill Climbing Search.
# Takes in a Graph Problem and solves with Hill Climbing Search.
def do_hill_climbing(problem):
    path = SPSA.hill_climbing(problem)
    if "Plateau" in path:
        print("Local minimum found. Search incomplete.")
        path.remove("Plateau")
    print("Using the Hill Climbing Method")
    print("The total cost of the path was " + str(path[-1].path_cost))
    print("The path was " + path[0].state, end=" ")
    for i in range(1, len(path)):
        print("to " + path[i].state, end=" ")
    print("\n")

# Helper function used to call Simulated Annealing Search.
# Takes in a Graph Problem and solves with Simulated Annealing Search.
def do_simulated_annealing(problem):
    path = SPSA.simulated_annealing(problem)
    if "Plateau" in path:
        print("Search incomplete.")
        path.remove("Plateau")
    print("Using the Simulated Annealing Method")
    print("The total cost of the path was " + str(path[-1].path_cost))
    print("The path was " + path[0].state, end=" ")
    for i in range(1, len(path)):
        print("to " + path[i].state, end=" ")
    print("\n")

def main():
    # Load the map file.
    file = input('Please enter the location of your map file: ')
    file_exists = os.path.exists(file)
    while file_exists != True:
        file = input('Please enter valid file name (or exit to quit): ')
        file_exists = os.path.exists(file)
        if file.lower() == 'exit':
            return
    romania_map = readMap(file)

    # Loop to run the code until the user would like to exit the program.
    run_again = True
    print("\n" + "Hello, where will you be traveling in Romania?")
    while(run_again):

        # Ask user for cities they would like to find a path between.
        cityOne = input("Enter the first city: ")
        cityTwo = input("Enter the second city: ")
        print()

        # Check to see if cities are valid.
        # If not, prompt user to re-enter cities or allow them to exit.
        while checkCities(cityOne,cityTwo, romania_map):
            print()
            print("Please enter valid (and different) cities...")
            cityOne = input("Enter the first city: (or exit to quit) ")
            if cityOne.lower() == 'exit':
                return
            cityTwo = input("Enter the second city: (or exit to quit) ")
            if cityTwo.lower() == 'exit':
                return

        # Create Graph Problem instance.
        gp = SPSA.GraphProblem(cityOne, cityTwo, romania_map)
        # Run GBFS Search.
        do_gbfs(gp)
        # Run A* Search.
        do_astar(gp)
        # Run Hill Climbing Search.
        do_hill_climbing(gp)
        # Run Simulated Annealing Search.
        do_simulated_annealing(gp)

        # Once search is completed...
        # Allow user the option to search for a path between a new pair or cities or exit.
        again = input('Would you like to check another pair of cities? ')
        again = inputTest(again)
        if again is None:
            return
        if again.lower() == 'yes':
            print()
        else:
            print("Thank You for Using Our App.")
            run_again = False

if __name__ == "__main__":
    main()