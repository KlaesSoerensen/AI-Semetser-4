def compute_viterbi(states: ndarray, observations: list[int | None], a_transitions: ndarray, b_emissions: ndarray):
    # number of states - subtract two because "initial" and "final" doesn't count.
    big_n = len(states) - 2

    # number of observations - subtract one, because a dummy "None" is added on index 0.
    big_t = len(observations) - 1

    # final state
    qf = big_n + 1

    # probability matrix - initialize with zeros
    viterbi = np.zeros((big_n + 2, big_t + 1))

    # backpointer matrix
    backpointers = np.zeros((big_n + 2, big_t + 1), dtype=int)

    # Initial state probabilities
    viterbi[0, 0] = 1.0

    # Compute Viterbi probabilities and backpointers
    for t in range(1, big_t + 1):
        for j in range(1, big_n + 1):
            max_prob, max_state = max((viterbi[i, t - 1] * a_transitions[i, j] * b_emissions[j, observations[t]], i) for i in range(big_n + 2))
            viterbi[j, t] = max_prob
            backpointers[j, t] = max_state

    # Trace back the path
    path = [0] * (big_t + 1)
    max_final_prob, path[big_t] = max((viterbi[j, big_t] * a_transitions[j, qf], j) for j in range(1, big_n + 1))

    for t in range(big_t, 0, -1):
        path[t - 1] = backpointers[path[t], t]

    return path
