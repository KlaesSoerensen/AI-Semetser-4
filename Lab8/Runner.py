from pprint import pformat
from Variable import Variable
from bn import BayesianNetwork

def pad(string: str, pad: int = 4) -> str:
    """Adds spaces at the beginning of each line in the string for indentation."""
    lines = string.split('\n')
    padded_lines = (' ' * pad + line for line in lines)
    return '\n'.join(padded_lines)

def print_conditional_probability(network: BayesianNetwork, conditionals_vars: dict[str, str],
                                  conditionals_evidents: dict[str, str]) -> float:
    """Prints and returns the conditional probability given the evidences."""
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    prob = network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )
    print("is {:f}".format(prob))
    print()
    return prob

def print_joint_probability(network: BayesianNetwork, values: dict[str, str]) -> None:
    """Prints the joint probability of a given set of values."""
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))

def print_marginal_probabilities(network: BayesianNetwork) -> None:
    """Prints the marginal probabilities for each variable in the network."""
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )

def define_model() -> BayesianNetwork:
    """Defines the Bayesian network model.
    Modify this function to change the model structure and CPTs (Conditional Probability Tables)."""

    # Define the probability tables for each variable
    # Format: {tuple_of_parent_values: tuple_of_probabilities}
    dt_probabilities = {(): (0.3, 0.7)}  # Probability of Damaged Tire (DT)
    ftl_probabilities = {(): (0.2, 0.8)}  # Probability of Fuel Tank Leaking (FTL)
    em_probabilities = {(): (0.3, 0.7)}  # Probability of Electronics Malfunctioning (EM)
    sms_probabilities = {('T', 'T'): (0.05, 0.95), ('T', 'F'): (0.6, 0.4),
                         ('F', 'T'): (0.3, 0.7), ('F', 'F'): (0.7, 0.3)}  # Probability of Slow Max Speed (SMS)
    v_probabilities = {('T',): (0.7, 0.3), ('F',): (0.1, 0.9)}  # Probability of Vibrations (V)
    hc_probabilities = {('T', 'T', 'T'): (0.9, 0.1), ('T', 'T', 'F'): (0.8, 0.2),
                        ('T', 'F', 'T'): (0.3, 0.7), ('T', 'F', 'F'): (0.2, 0.8),
                        ('F', 'T', 'T'): (0.6, 0.4), ('F', 'T', 'F'): (0.5, 0.5),
                        ('F', 'F', 'T'): (0.1, 0.9), ('F', 'F', 'F'): (0.01, 0.99)}  # Probability of High Consumption (HC)

    # Create the variable objects
    # Format: Variable(name, ('F', 'T'), probability_table, [list_of_parents])
    dt = Variable('DT', ('F', 'T'), dt_probabilities)
    ftl = Variable('FTL', ('F', 'T'), ftl_probabilities)
    em = Variable('EM', ('F', 'T'), em_probabilities)
    sms = Variable('SMS', ('F', 'T'), sms_probabilities, [dt, em])
    v = Variable('V', ('F', 'T'), v_probabilities, [dt])
    hc = Variable('HC', ('F', 'T'), hc_probabilities, [dt, ftl, em])

    variables = [dt, ftl, em, sms, v, hc]

    # Create and return the Bayesian network
    network = BayesianNetwork()
    network.set_variables(variables)
    return network

def define_observations() -> dict[str, str]:
    """Defines the observed variables (symptoms).
    Modify this function to change the observed variables."""
    # Here you must put observed value
    # Format: {'VariableName': 'ObservedValue'}
    return {'V': 'T', 'SMS': 'T', 'HC': 'F'}

def car_malfunction_network():
    """Main function to run the Bayesian network analysis."""
    network = define_model()

    # Pre-calculate marginals
    network.calculate_marginal_probabilities()

    # Print the marginal probabilities
    print_marginal_probabilities(network)
    print('')

    # Example joint probability calculation
    joint_values = {
        'DT': 'F',
        'FTL': 'F',
        'EM': 'F',
        'SMS': 'T',
        'V': 'T',
        'HC': 'F'
    }
    print_joint_probability(network, joint_values)
    print('')

    # Define observed variables
    observed_vars = define_observations()

    # Calculate conditional probabilities for possible causes
    conditionals_vars = {'DT': 'T'}  # Here you must put the variable you want to test as the cause
    dt_prob = print_conditional_probability(network, conditionals_vars, observed_vars)

    conditionals_vars = {'FTL': 'T'}  # Here you must put the variable you want to test as the cause
    ftl_prob = print_conditional_probability(network, conditionals_vars, observed_vars)

    conditionals_vars = {'EM': 'T'}  # Here you must put the variable you want to test as the cause
    em_prob = print_conditional_probability(network, conditionals_vars, observed_vars)

    # Determine and print the most likely cause
    most_likely_cause = max(
        (dt_prob, 'Damaged Tire'),
        (ftl_prob, 'Fuel Tank Leaking'),
        (em_prob, 'Electronics Malfunctioning')
    )[1]
    print(f"Most likely cause given symptoms: {most_likely_cause}")

if __name__ == '__main__':
    car_malfunction_network()
