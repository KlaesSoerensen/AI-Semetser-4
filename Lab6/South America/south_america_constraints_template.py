from typing import List, Dict
from south_america_colors import Color
from collections.abc import Callable
from south_america_states import States

type contraintFunction = Callable[[States, Color, States, Color], bool]
type Assignment = dict[States, Color]

class CSP:
    def __init__(self, variables: list[States], domains: dict[States, list[Color]],
                 neighbours: dict[States, list[States]], constraints: dict[States, contraintFunction]):
        self.variables: List[States] = variables
        self.domains: Dict[States, List[Color]] = domains
        self.neighbours: Dict[States, List[States]] = neighbours
        self.constraints: Dict[States, contraintFunction] = constraints

    def backtracking_search(self) -> dict[States, Color] | None:
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment: Assignment) -> Dict[States, Color]:
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                del assignment[var]

        return None

    def select_unassigned_variable(self, assignment: Assignment) -> States:
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment: Assignment) -> bool:
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable: States, assignment: Assignment) -> list[Color]:
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable: States, value: Color, assignment: Assignment) -> bool:
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_south_america_csp() -> CSP:
    # List all countries as variables
    variables = [
        States.Colombia, States.Venezuela, States.Guyana, States.Suriname,
        States.Guyane_Fr, States.Ecuador, States.Peru, States.Brasil,
        States.Bolivia, States.Paraguay, States.Chile, States.Argentina, States.Uruguay
    ]
    values = [Color.Red, Color.Blue, Color.Green, Color.Yellow]
    domains = {country: values[:] for country in variables}
    neighbours = {
        States.Colombia: [States.Venezuela, States.Ecuador, States.Brasil, States.Peru],
        States.Venezuela: [States.Colombia, States.Guyana, States.Brasil],
        States.Guyana: [States.Venezuela, States.Suriname, States.Brasil],
        States.Suriname: [States.Guyana, States.Guyane_Fr, States.Brasil],
        States.Guyane_Fr: [States.Suriname, States.Brasil],
        States.Ecuador: [States.Colombia, States.Peru],
        States.Peru: [States.Ecuador, States.Colombia, States.Brasil, States.Bolivia, States.Chile],
        States.Brasil: [States.Guyane_Fr, States.Suriname, States.Guyana, States.Venezuela, States.Colombia,
                        States.Peru, States.Bolivia, States.Paraguay, States.Argentina, States.Uruguay],
        States.Bolivia: [States.Peru, States.Brasil, States.Paraguay, States.Argentina, States.Chile],
        States.Paraguay: [States.Brasil, States.Bolivia, States.Argentina],
        States.Chile: [States.Peru, States.Bolivia, States.Argentina],
        States.Argentina: [States.Chile, States.Bolivia, States.Paraguay, States.Brasil, States.Uruguay],
        States.Uruguay: [States.Brasil, States.Argentina],
    }

    def constraint_function(first_variable: States, first_value: Color, second_variable: States, second_value: Color) -> bool:
        """Returns true if neighboring variables have different values."""
        return first_value != second_value or first_variable == second_variable

    constraints = {country: constraint_function for country in variables}

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_south_america_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
