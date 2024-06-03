import random
from typing import List

from ga import Individual, genetic_algorithm

class SimpleIndividual(Individual):
    def __init__(self, dna: List[int]):
        self.dna = dna

    def get_fitness(self) -> float:
        return sum(self.dna)

    def mutate(self):
        mutation_index = random.randint(0, len(self.dna) - 1)
        self.dna[mutation_index] = 1 - self.dna[mutation_index]

    def reproduce(self, other: 'SimpleIndividual') -> 'SimpleIndividual':
        crossover_index = random.randint(0, len(self.dna) - 1)
        new_dna = self.dna[:crossover_index] + other.dna[crossover_index:]
        return SimpleIndividual(new_dna)

if __name__ == "__main__":
    initial_population = {SimpleIndividual([random.randint(0, 1) for _ in range(10)]) for _ in range(20)}

    fittest = genetic_algorithm(initial_population, minimal_fitness=5)

    print(f"The fittest individual is: {fittest}")
