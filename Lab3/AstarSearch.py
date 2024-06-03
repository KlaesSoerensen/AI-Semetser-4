import heapq

class Node:
    def __init__(self, name, heuristic):
        self.name = name
        self.heuristic = heuristic
        self.adjacent = {}  # Neighbors with edge costs
        self.parent = None

    def add_edge(self, neighbor, cost):
        self.adjacent[neighbor] = cost

    def __lt__(self, other):
        return self.heuristic < other.heuristic

nodes = {
    'A': Node('A', 6),
    'B': Node('B', 5),
    'C': Node('C', 5),
    'D': Node('D', 2),
    'E': Node('E', 4),
    'F': Node('F', 5),
    'G': Node('G', 4),
    'H': Node('H', 1),
    'I': Node('I', 2),
    'J': Node('J', 1),
    'K': Node('K', 0),
    'L': Node('L', 0)
}

edges = [
    ('A', 'B', 1), ('A', 'C', 2), ('A', 'D', 4),
    ('B', 'E', 4), ('B', 'F', 5), ('C', 'E', 1),
    ('D', 'I', 2), ('E', 'G', 2), ('E', 'H', 3),
    ('F', 'G', 1), ('G', 'K', 6), ('H', 'K', 4),
    ('I', 'J', 3), ('J', 'L', 3), ('H', 'L', 5)
]

for edge in edges:
    nodes[edge[0]].add_edge(nodes[edge[1]], edge[2])
    nodes[edge[1]].add_edge(nodes[edge[0]], edge[2])


def greedy_best_first_search(start, goal_nodes):
    open_list = [(start.heuristic, start)]
    closed_set = set()

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node in closed_set:
            continue

        if current_node.name in goal_nodes:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        for adj, cost in current_node.adjacent.items():
            if adj not in closed_set:
                adj.parent = current_node
                heapq.heappush(open_list, (adj.heuristic, adj))

    return None

def a_star_search(start, goal_nodes, weight=1):
    open_list = [(start.heuristic, start)]
    closed_set = set()
    g_costs = {start: 0}

    while open_list:
        _, current_node = heapq.heappop(open_list)

        if current_node in closed_set:
            continue

        if current_node.name in goal_nodes:
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node)

        for adj, cost in current_node.adjacent.items():
            if adj in closed_set and g_costs[adj] <= g_costs[current_node] + cost:
                continue

            adj.parent = current_node
            g_costs[adj] = g_costs[current_node] + cost
            f_cost = g_costs[adj] + weight * adj.heuristic
            heapq.heappush(open_list, (f_cost, adj))

    return None

# Define the list of goal nodes
goal_nodes = ['K', 'L']

# Run both searches from node A to the closest goal node
greedy_path_to_closest_goal = greedy_best_first_search(nodes['A'], goal_nodes)
a_star_path_to_closest_goal = a_star_search(nodes['A'], goal_nodes)

# Print the updated results
print("Greedy Best First Search path to closest goal:", greedy_path_to_closest_goal)
print("A* Search path to closest goal:", a_star_path_to_closest_goal)

# Return the paths for use outside of print if needed
(greedy_path_to_closest_goal, a_star_path_to_closest_goal)

