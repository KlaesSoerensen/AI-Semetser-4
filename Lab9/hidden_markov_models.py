import numpy as np
from numpy import ndarray

"""
Hidden Markov Model using Viterbi algorithm to find the most
likely sequence of hidden states.
"""

def main():
    np.set_printoptions(suppress=True)
    states = np.array(["start", "hot", "cold", "end"])

    # Observation sequences: add a dummy None at the beginning
    observation_sets = [
        [None, 2, 1, 3, 1],
    ]

    # Transition probability matrix
    # transitions[current][next]
    # States: start (0), hot (1), cold (2), end (3)
    transitions = np.array([
        [.0, .6, .4, .0],  # Start
        [.0, .3, .5, .2],  # Hot
        [.0, .2, .6, .2],  # Cold
        [.0, .0, .0, .0],  # End
    ])

    # Emission probability matrix
    # emissions[state][observation]
    # States: start (0), hot (1), cold (2), end (3)
    # Observations: 0, 1, 2, 3 ice creams
    emissions = np.array([
        [.0, .0, .0, .0],  # Start
        [.0, .2, .5, .3],  # Hot
        [.0, .4, .3, .3],  # Cold
        [.0, .0, .0, .0],  # End
    ])

    for observations in observation_sets:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))
        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))
        path = compute_viterbi(states, observations, transitions, emissions)
        print(f"Path: {convert_path_states_to_observations(path, states)}")
        print('')

def convert_path_states_to_observations(path: list[int], states: ndarray[str]) -> list[str]:
    return [states[p] for p in path]

def inclusive_range(a: int, b: int) -> range:
    return range(a, b + 1)

def compute_forward(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray[float]) -> float:
    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf: int = big_n + 1
    forward: ndarray = np.zeros((big_n + 2, big_t + 1))
    forward[0, 0] = 1.0

    for t in range(1, big_t + 1):
        for j in range(1, big_n + 1):
            forward[j, t] = sum(forward[i, t - 1] * a_transitions[i, j] * b_emissions[j, observations[t]] for i in range(big_n + 2))

    probability = sum(forward[j, big_t] * a_transitions[j, qf] for j in range(1, big_n + 1))
    return probability

def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray):
    big_n = len(states) - 2
    big_t = len(observations) - 1
    qf = big_n + 1
    viterbi = np.zeros((big_n + 2, big_t + 1))
    backpointers = np.zeros((big_n + 2, big_t + 1), dtype=int)
    viterbi[0, 0] = 1.0

    for t in range(1, big_t + 1):
        for j in range(1, big_n + 1):
            max_prob, max_state = max((viterbi[i, t - 1] * a_transitions[i, j] * b_emissions[j, observations[t]], i) for i in range(big_n + 2))
            viterbi[j, t] = max_prob
            backpointers[j, t] = max_state

    path = [0] * (big_t + 1)
    max_final_prob, path[big_t] = max((viterbi[j, big_t] * a_transitions[j, qf], j) for j in range(1, big_n + 1))

    for t in range(big_t, 0, -1):
        path[t - 1] = backpointers[path[t], t]

    return path

def argmax(sequence: list[tuple[float, float]]):
    return max(sequence, key=lambda x: x[1])[0]

if __name__ == '__main__':
    main()
