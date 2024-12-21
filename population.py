from genome import CubeGenome
import random
import numpy as np

class Population:
    def __init__(self, size, start, end_goal):
        self.size = size
        self.genomes = [CubeGenome() for _ in range(size)]
        self.start = start
        self.end_goal = end_goal

    def fitness(self):
        return [genome.fitness(self.start, self.end_goal) for genome in self.genomes]

    def selection(self):
        next_gen = []
        # Death if you do nothing
        self.genomes = [genome for genome in self.genomes if len(genome.genome) > 0]
        fitness_scores = self.fitness()
        
        sorted_genomes = [genome for _, genome in sorted(zip(fitness_scores, self.genomes), key=lambda x: x[0], reverse=True)]
        top_n = 5
        # Maintain top 5 genomes
        next_gen.extend(sorted_genomes[:top_n])
        weights = 1 / (1 + np.exp(-np.array(fitness_scores)))
        # # Roulette wheel selection
        # for genome in self.genomes:
        #     next_gen.append(genome.crossover(random.choices(sorted_genomes, weights=weights, k=1)[0]))
        # Ranked selection
        for genome in self.genomes:
            next_gen.append(genome.crossover(random.choices(sorted_genomes, weights=range(1, len(sorted_genomes) + 1), k=1)[0]))
        
        self.genomes = [genome for genome in next_gen if len(genome.genome) > 0]
        next_gen_fitnesses = self.fitness()
        fitness_threshold = np.percentile(next_gen_fitnesses, 5)
        self.genomes = [genome for genome in self.genomes if genome.fitness(self.start, self.end_goal) >= fitness_threshold]


        
        

    def mutation(self):
        for genome in self.genomes:
            genome.mutate()
        

    def evolve(self):
        self.selection()
        self.mutation()
