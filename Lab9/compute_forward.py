import numpy as np
from numpy import ndarray


def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray,
                    b_emissions: ndarray[float]) -> float:
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf: int = big_n + 1

    # probability matrix - initialize with zeros
    forward: ndarray = np.zeros((big_n + 2, big_t + 1))

    # Initial state probabilities
    forward[0, 0] = 1.0

    # Compute forward probabilities
    for t in range(1, big_t + 1):
        for j in range(1, big_n + 1):
            forward[j, t] = sum(forward[i, t - 1] * a_transitions[i, j] * b_emissions[j, observations[t]] for i in range(big_n + 2))

    # Sum probabilities in final state
    probability = sum(forward[j, big_t] * a_transitions[j, qf] for j in range(big_n + 2))

    return probability
