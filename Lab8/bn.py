import functools
from Variable import Variable


def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """

    def mult(x, y):
        return x * y

    return functools.reduce(mult, vector, 1)


class BayesianNetwork(object):
    """ Bayesian Network implementation. This implementation incorporates few
        assumptions (see comments).
    """

    def __init__(self):
        """ Initialize connectivity matrix. """
        self.variables: list[Variable] = []  # list of variables (Nodes)
        self.variable_dictionary: dict[
            str, Variable] = {}  # a mapping of variable name to the actual node, for easy access
        self.ready: bool = False  # indication of this net state

    def calculate_marginal_probabilities(self) -> None:
        """ pre-calculate and stores the marginal probabilities of all the nodes """
        # iterate over the Nodes, from parents to children
        for variable in self.variables:
            variable.calculate_marginal_probability()
        self.ready = True

    def get_variables(self) -> list[Variable]:
        """ returns the variables """
        return self.variables

    def get_variable(self, variable_name: str) -> Variable:
        """ returns the variable with the given name """
        return self.variable_dictionary[variable_name]

    def add_variable(self, var: Variable, index: int = -1) -> None:
        """ add a single Node to the net """
        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)
        self.variable_dictionary[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def set_variables(self, new_variables: list[Variable]) -> None:
        """ quick assignment: set the given Node list to be the Nodes of this net """
        self.variables = new_variables
        for variable in self.variables:
            self.variable_dictionary[variable.name] = variable
        self.ready = False  # we need to re-calculate marginals
        self.calculate_marginal_probabilities()

    def get_marginal_probability(self, var: Variable, val: str) -> float:
        """ returns the marginal probability of a given node """
        return var.get_marginal_probability(val)

    def get_joint_probability(self, values: dict[str, str]) -> float:
        """ return the joint probability of the Nodes """
        joint_prob = 1.0
        for variable_name, value in values.items():
            variable = self.variable_dictionary[variable_name]
            parent_values = {parent.name: values[parent.name] for parent in variable.parents if parent.name in values}
            joint_prob *= variable.get_conditional_probability(value, parent_values)
        return joint_prob

    def get_conditional_probability(self, values: dict[str, str], evidents: dict[str, str]) -> float:
        """ returns the conditional probability.
            This method implements simple inference: the joint probability of children given their parents
            or the probability of parents given their children.
            Assumption: variables in each level are independent, or independent given their parents
            (i.e. vars in values are independent, as well as vars in evidents)
        """
        joint_prob_evidents_and_values = self.get_joint_probability({**values, **evidents})
        joint_prob_evidents = self.get_joint_probability(evidents)

        if joint_prob_evidents == 0:
            return 0

        return joint_prob_evidents_and_values / joint_prob_evidents

    def sub_vals(self, var: Variable, values: dict[str, str]) -> tuple[str, ...]:
        """ return a tuple, contain all the relevant
            assignments for the given variable (i.e - the assignments
            pertaining to the variable`s parents."""
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)
