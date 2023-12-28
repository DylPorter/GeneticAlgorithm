import random
# import pygame
#
#WIDTH = 100
#HEIGHT = 100
#
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))

MIN_FITNESS = 16
GENOME_LENGTH = 8
POP_SIZE = 20
# should you pass global constants in functions?


class Organism:
    def __init__(self):
        self.genome = []
        self.fitness = 0
        self.location = [0, 0]

    def initialise_genome(self):
        for x in range(GENOME_LENGTH):
            self.genome.append(random.randint(0,4))

    def single_point_crossover(self, genome1, genome2):
        crossover_point = random.randint(1, GENOME_LENGTH-1)
        new_genome = []
        print(genome1, genome2, crossover_point)

        for x in range(0, crossover_point):
            new_genome.append(genome1[x])

        for y in range(crossover_point, GENOME_LENGTH):
            new_genome.append(genome2[y])

        self.genome = new_genome

#    def spawn_position(self):
#        self.location = [random.randint(0, WIDTH), random.randint(0, HEIGHT)]
#
#    def movement(genome):
#        for x in genome:
#            if x == 0:
#                self.location[0] += 1  # Move Up
#            elif x == 1:
#                self.location[0] -= 1  # Move Down
#            elif x == 2:
#                self.location[1] += 1  # Move Right
#            elif x == 3:
#                self.location[2] -= 1  # Move Left
#            elif x == 4:
#                pass  # Do Nothing


def main():

    # Initialise population
    population = []
    generate_population(population)
    
    # Population fitness & selection
    population, fitness = calculate_fitness(population)
    print(fitness)
    print("Survivors:", len(population))

    # Find pairs of fit organisms to initialise new organisms and genomes
    for x in range(POP_SIZE-len(population)):
        repopulate(population, select_pair(population, fitness))
        

    # Population offspring
     
        # Crossover
        # Mutation


#    running = True
#    clock = pygame.time.Clock()
#
#    while running:
#        clock.tick(60)
#        screen.fill(0,0,0)
#        pygame.display.update()
#
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                running = False
#    pygame.quit()


def generate_population(population):
    for x in range(POP_SIZE):
        population.append(Organism())
        population[x].initialise_genome()


def calculate_fitness(population):
    pool = []
    weights = []

    for x in range(len(population)):
        fitness = sum(population[x].genome)
        if fitness >= MIN_FITNESS:
            pool.append(population[x])
            weights.append(fitness)
            population[x].fitness = fitness

    return pool, weights


def select_pair(pool, weights):
    pair = []

    while len(pair) < 2:
        selection = random.choices(pool, weights = weights, k = 1)
        if selection not in pair:
            pair.append(selection)

    return pair

def repopulate(pop_list, parent):
    new_organism = Organism()
    new_organism.single_point_crossover(parent[0][0].genome, parent[1][0].genome)

    print(new_organism.genome)
    #pop_list.append(new_organism)

if __name__ == "__main__":
    main()
