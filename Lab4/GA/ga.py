import random
from typing import Set, Tuple
from abc import ABC, abstractmethod

default_p_mutation = 0.8
default_num_of_generations = 30
max_population_size = 100

class Individual(ABC):
    @abstractmethod
    def get_fitness(self) -> float:
        pass

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def reproduce(self, other: 'Individual') -> 'Individual':
        pass

    def __lt__(self, other: 'Individual') -> bool:
        return self.get_fitness() < other.get_fitness()

    def __repr__(self):
        return f"Fitness: {self.get_fitness()}"

def genetic_algorithm(population: Set[Individual], minimal_fitness: float,
                      num_of_generations: int = default_num_of_generations,
                      should_trim_population: bool = False,
                      p_mutation=default_p_mutation) -> Individual | None:
    for generation in range(num_of_generations):
        print(f"Generation {generation}:")
        print_population(population)

        new_population: Set[Individual] = set()

        for _ in population:
            mother, father = random_selection(population)
            child = mother.reproduce(father)
            if random.random() < p_mutation:
                child.mutate()
            new_population.add(child)

        population = population.union(new_population)

        if should_trim_population:
            population = trim_population(population, max_population_size)

        fittest_individual = get_fittest_individual(population)
        if fittest_individual and minimal_fitness <= fittest_individual.get_fitness():
            break

    print(f"Final generation {generation}:")
    print_population(population)
    return fittest_individual

def print_population(population: Set[Individual]) -> None:
    if len(population) > 10:
        print(f"Population too large to print {len(population)}, fittest individual: {get_fittest_individual(population)}")
    else:
        for individual in population:
            print(individual)

def random_selection(population: Set[Individual]) -> Tuple[Individual, Individual]:
    total_fitness = sum(individual.get_fitness() for individual in population)
    individuals = random.choices(list(population), weights=[ind.get_fitness() for ind in population], k=2)
    return tuple(individuals)

def get_fittest_individual(population: Set[Individual]) -> Individual:
    return max(population, key=lambda ind: ind.get_fitness(), default=None)

def trim_population(population: Set[Individual], desired_length: int) -> Set[Individual]:
    return set(sorted(population, key=lambda ind: ind.get_fitness(), reverse=True)[:desired_length])


