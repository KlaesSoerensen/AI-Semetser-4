import heapq
from Enums import States, Location, Action
from typing import List, Tuple, Dict

class State:
    def __init__(self, vacuum_location: Location, locations: Dict[Location, States], path_cost: int, parent=None, action=None):
        self.vacuum_location = vacuum_location
        self.locations = locations
        self.path_cost = path_cost
        self.parent = parent  # The state from which this state was reached
        self.action = action  # The action that was taken to reach this state

    def is_goal(self) -> bool:
        return all(status == States.CLEAN for status in self.locations.values())

    def successors(self) -> List[Tuple['State', Action]]:
        successors = []
        for action in self.vacuum_location.allowed_moves():
            new_location = self._move(self.vacuum_location, action)
            new_locations = self.locations.copy()
            if action == Action.SUCK:
                new_locations[self.vacuum_location] = States.CLEAN
            new_state = State(new_location, new_locations, self.path_cost + 1, self, action)
            successors.append((new_state, action))
        return successors

    def _move(self, location: Location, action: Action) -> Location:
        if action == Action.RIGHT and action in location.allowed_moves():
            return Location.B
        elif action == Action.DOWN and action in location.allowed_moves():
            return Location.C
        elif action == Action.LEFT and action in location.allowed_moves():
            return Location.D
        elif action == Action.UP and action in location.allowed_moves():
            return Location.A
        return location

    def heuristic(self) -> int:
        return sum(1 for status in self.locations.values() if status == States.DIRTY)

    def __lt__(self, other):
        return (self.path_cost + self.heuristic()) < (other.path_cost + other.heuristic())

def a_star_search(initial_state: State) -> Tuple[List[Action], int]:
    frontier = [(initial_state.heuristic(), initial_state)]
    explored = set()
    while frontier:
        _, current_state = heapq.heappop(frontier)
        if current_state.is_goal():
            return current_state.path_cost, reconstruct_path(current_state)
        explored.add(current_state)
        for successor, action in current_state.successors():
            if successor not in explored:
                heapq.heappush(frontier, (successor.path_cost + successor.heuristic(), successor))
    return None

def reconstruct_path(state: State) -> List[Action]:
    actions = []
    while state.parent is not None:
        actions.append(state.action)
        state = state.parent
    actions.reverse()  # The actions are added in reverse order so we need to reverse them at the end
    return actions

initial_state = State(Location.A, {
    Location.A: States.DIRTY,
    Location.B: States.DIRTY,
    Location.C: States.DIRTY,
    Location.D: States.DIRTY
}, path_cost=0)

cost, path = a_star_search(initial_state)
print(f"Path to the goal: {path}")
print(f"Cost of the path: {cost}")
