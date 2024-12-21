from population import Population
import magiccube
from cube_utils import get_cube_state

solved_cube = magiccube.Cube(3, "YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")

solved_cube.rotate("R U R'")

resulting_state = get_cube_state(solved_cube)

pop = Population(400, resulting_state, "YYYYYYYYYRRRRRRRRRGGGGGGGGGOOOOOOOOOBBBBBBBBBWWWWWWWWW")


if __name__ == "__main__":  
    for i in range(100):
        pop.evolve()
        if i % 10 == 0:
            print(f"Generation {i}")
            print(f"Population size: {len(pop.genomes)}")
            print(f"Top 5 fitness: {sorted(pop.fitness(), reverse=True)[:5]}")
            print(f"Best solution: {pop.genomes[0]}")
