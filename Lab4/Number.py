import random
from typing import Self

from Lab4.GA.ga import Individual, genetic_algorithm


class NumberIndividual(Individual):
    def __init__(self, gene: tuple):
        self.gene = gene

    def get_fitness(self) -> float:
        return sum(val * (2 ** idx) for idx, val in enumerate(reversed(self.gene)))

    def mutate(self) -> Self:
        index_to_mutate = random.randint(0, len(self.gene) - 1)
        mutated_gene = list(self.gene)
        mutated_gene[index_to_mutate] = 1 if self.gene[index_to_mutate] == 0 else 0
        self.gene = tuple(mutated_gene)
        return self

    def reproduce(self, other: 'NumberIndividual') -> 'NumberIndividual':
        crossover_point = random.randint(1, len(self.gene) - 1)
        child_gene = self.gene[:crossover_point] + other.gene[crossover_point:]
        return NumberIndividual(child_gene)

    def __hash__(self):
        return hash(self.gene)

    @classmethod
    def create_random(cls, length_of_gene: int) -> Self:
        return cls(tuple(random.randint(0, 1) for _ in range(length_of_gene)))

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"


def get_initial_population(n: int, count: int) -> set[NumberIndividual]:
    """
    Randomly generate count individuals of length n
    Note since it's a set it disregards duplicate elements.

    Be aware that since the individuals are generated randomly, but duplicates are not allowed.
    It can take a long time if you use large numbers of count and n together.
    """

    if count > 2 ** n:
        raise ValueError("Count must be less than 2^n, otherwise not enough unique individuals can be generated.")

    out: set[NumberIndividual] = set()

    while len(out) < count:
        out.add(NumberIndividual.create_random(n))

    return out


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        NumberIndividual((1, 1, 0)),
        NumberIndividual((0, 0, 0)),
        NumberIndividual((0, 1, 0)),
        NumberIndividual((1, 0, 0))
    }
    # initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, minimal_fitness)
    print('Fittest Individual: ' + str(fittest))


if __name__ == '__main__':
    main()
