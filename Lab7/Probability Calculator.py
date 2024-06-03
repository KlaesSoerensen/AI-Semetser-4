def calculate_conditional_probability(p_condition, p_positive_given_condition, p_positive_given_no_condition):
    """
    Calculate the conditional probability of a condition being true given a positive result,
    based on Bayes' theorem. This function can be applied to a wide range of scenarios.

    Parameters:
    p_condition: The prior probability of the condition being true, P(Condition).
    p_positive_given_condition: The probability of testing positive if the condition is true,
    P(Positive|Condition).
    p_positive_given_no_condition: The probability of testing positive if the
    condition is not true, P(Positive|NoCondition).
    """

    # Calculate the complement of the prior probability, P(NoCondition)
    p_no_condition = 1 - p_condition

    # Calculate the total probability of testing positive, P(Positive)
    p_positive = (p_positive_given_condition * p_condition) + (p_positive_given_no_condition * p_no_condition)

    # Calculate the conditional probability, P(Condition|Positive)
    p_condition_given_positive = (p_positive_given_condition * p_condition) / p_positive

    return p_condition_given_positive


# Example usage:
p_condition_given_positive_a = calculate_conditional_probability(0.01, 0.95, 0.10)
p_condition_given_positive_b = calculate_conditional_probability(0.01, 0.90, 0.05)
print("Probability of the condition being true given a positive result (Test A):", p_condition_given_positive_a)
print("Probability of the condition being true given a positive result (Test B):", p_condition_given_positive_b)

p_condition_given_positive = calculate_conditional_probability(0.0001, 0.99, 0.01)
print("Probability of the condition being true given a positive result:", p_condition_given_positive)
