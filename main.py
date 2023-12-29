import random
import pygame

WIDTH = 1000
HEIGHT = 1000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# should you pass global constants in functions?
MIN_FITNESS = 10
GENOME_LENGTH = 8
POP_SIZE = 100  # Algorithm runs slowly with large population sizes (i.e. 1000+)
MUTATION_CHANCE = 0.01


class Organism:
    def __init__(self):
        self.genome = []
        self.fitness = 0
        # self.location = [0, 0]

    def initialise_genome(self):
        for i in range(GENOME_LENGTH):
            self.genome.append(random.randint(0, 4))

    def calculate_fitness(self):
        fitness = sum(self.genome)

        if fitness >= MIN_FITNESS:
            self.fitness = fitness
            return True

    def single_crossover(self, genome1, genome2):
        crossover_point = random.randint(1, GENOME_LENGTH - 1)
        new_genome = []
        # print(genome1, genome2, crossover_point)

        for i in range(0, crossover_point):
            new_genome.append(genome1[i])

        for j in range(crossover_point, GENOME_LENGTH):
            new_genome.append(genome2[j])

        self.genome = new_genome

    def mutate_genome(self):
        index = random.randint(0, GENOME_LENGTH - 1)
        new_gene = self.genome[index]

        while self.genome[index] == new_gene:
            new_gene = random.randint(0, 4)

        self.genome[index] = new_gene

    def spawn_position(self):
        self.location = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]

    def movement(genome):
        for i in genome:
            if i == 0:
                self.location[0] += 1  # Move Up
            elif i == 1:
                self.location[0] -= 1  # Move Down
            elif i == 2:
                self.location[1] += 1  # Move Right
            elif i == 3:
                self.location[2] -= 1  # Move Left
            elif i == 4:
                pass                   # Do Nothing


class StateMachine:
    def __init__(self):
        self.load_state = "visualiser"
        self.running = True
        self.clock = pygame.time.Clock()

    def run_algorithm(self, population, count):
        # Population fitness & selection
        fitness = []
        population = population_selection(population, fitness)

        print(sorted(fitness))
        print(f"Survivors: {len(population)} (Gen {count})")

        # Find pairs of fit organisms to generate new offspring
        new_population = []

        for i in range(POP_SIZE):
            child = generate_offspring(select_pair(population, fitness))
            new_population.append(child)

        population = new_population
        count += 1

    def run_visualiser(self):
        screen.fill((255, 255, 255))

    def main(self):
        # Generation counter
        count = 0

        # Generate the starting population
        population = []
        initialise_population(population)
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = false

            if self.load_state == "visualiser":
                self.run_visualiser()

            elif self.load_state == "algorithm":
                self.run_algorithm(population, count)
                self.load_state = "visualiser"

            pygame.display.flip()


def initialise_population(population):
    for i in range(POP_SIZE):
        population.append(Organism())
        population[i].initialise_genome()


def population_selection(population, fitness):
    pool = []

    for i in population:
        if i.calculate_fitness():
            pool.append(i)
            fitness.append(i.fitness)

    return pool


def select_pair(pool, weights):
    pair = []

    while len(pair) < 2:
        selection = random.choices(pool, weights=weights, k=1)
        if selection not in pair:   # KNOWN BUG: if pool of survivors is only 1
            pair.append(selection)

    return pair


def generate_offspring(parent):
    new_organism = Organism()

    new_organism.single_crossover(parent[0][0].genome, parent[1][0].genome)

    # Returns a float 0.0 <= x < 1.0 to determine mutation chance
    if random.random() < MUTATION_CHANCE:
        new_organism.mutate_genome()

    return new_organism


if __name__ == "__main__":
    app = StateMachine()
    app.main()
