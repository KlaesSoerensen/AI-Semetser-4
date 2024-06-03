import random
from typing import Set

class NumberIndividual:
    def __init__(self, gene: tuple):
        self.gene = gene

    def get_fitness(self) -> float:
        # Fitness is calculated as the decimal value of the binary gene
        return sum(val * (2 ** idx) for idx, val in enumerate(reversed(self.gene)))

    def mutate(self) -> 'NumberIndividual':
        index_to_mutate = random.randint(0, len(self.gene) - 1)
        mutated_gene = list(self.gene)
        mutated_gene[index_to_mutate] = 1 if self.gene[index_to_mutate] == 0 else 0
        self.gene = tuple(mutated_gene)
        return self

    def reproduce(self, other: 'NumberIndividual') -> 'NumberIndividual':
        crossover_point = random.randint(1, len(self.gene) - 1)
        child_gene = self.gene[:crossover_point] + other.gene[crossover_point:]
        return NumberIndividual(child_gene)

    @classmethod
    def create_random(cls, length_of_gene: int) -> 'NumberIndividual':
        return cls(tuple(random.randint(0, 1) for _ in range(length_of_gene)))

    def __repr__(self) -> str:
        return f"Gene: {self.gene} - Fitness: {self.get_fitness()}"

class SpecificNumberIndividual(NumberIndividual):
    def get_fitness(self) -> float:
        # Calculate the binary number's decimal value
        decimal_value = sum(val * (2 ** idx) for idx, val in enumerate(reversed(self.gene)))
        # Fitness should be the inverse of the absolute difference from the target number (4)
        return 1 / (1 + abs(decimal_value - 4))

    @classmethod
    def create_random(cls):
        # Create a random individual ensuring it's not the number 4 (100 in binary)
        while True:
            gene = tuple(random.randint(0, 1) for _ in range(3))
            if sum(val * (2 ** idx) for idx, val in enumerate(reversed(gene))) != 4:
                return cls(gene)

def genetic_algorithm(population: Set[NumberIndividual], minimal_fitness: float) -> NumberIndividual:
    max_generations = 100
    mutation_probability = 0.1
    fittest_individual = max(population, key=lambda ind: ind.get_fitness())

    for generation in range(max_generations):
        if fittest_individual.get_fitness() >= minimal_fitness:
            break

        new_population = set()
        population_list = list(population)  # Convert set to list for random sampling
        while len(new_population) < len(population):
            parent1, parent2 = random.sample(population_list, 2)
            child = parent1.reproduce(parent2)
            if random.random() < mutation_probability:
                child.mutate()
            new_population.add(child)

        population = new_population
        fittest_individual = max(population, key=lambda ind: ind.get_fitness())
        print(f"Generation {generation} - Fittest Individual: {fittest_individual}")

    return fittest_individual

def main():
    initial_population: Set[SpecificNumberIndividual] = {SpecificNumberIndividual.create_random() for _ in range(20)}
    fittest = genetic_algorithm(initial_population, minimal_fitness=1.0)  # Adjusted minimal fitness for clarity
    print(f"The fittest individual is: {fittest}")

main()
