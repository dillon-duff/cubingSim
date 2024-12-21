import random
import magiccube
from cube_utils import get_cube_state

# Genome
# A series of moves that can be annotated with:
# ' to indicate a counterclockwise move
# optionally the number 2 to indicate a double move


# Crossover types
# 1. Single point crossover


# Mutation types
# 1. Single move mutation
# 2. Reversal of a move
# 3. Reversal of a group of moves
# 4. Randomly insert a move
# 5. Duplicate a group of moves
# 6. Randomly remove a move
# 7. Randomly remove a group of moves
# 8. Randomly swap two moves
# 9. Randomly swap two groups of moves


# Fitness function
# Make every move in the genome and check if the cube is solved at every single step
# Reward more for being solved at the end of the genome
# Reward more for being solved in fewer moves

all_possible_moves = ["L", "L'", "L2", "R", "R'", "R2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'", "B2", "M", "M'", "M2", "E", "E'", "E2", "S", "S'", "S2"]

move_reversals = {"L": "L'", "L'": "L", "L2": "L2", "R": "R'", "R'": "R", "R2": "R2", "U": "U'", "U'": "U", "U2": "U2", "D": "D'", "D'": "D", "D2": "D2", "F": "F'", "F'": "F", "F2": "F2", "B": "B'", "B'": "B", "B2": "B2", "M": "M'", "M'": "M", "M2": "M2", "E": "E'", "E'": "E", "E2": "E2", "S": "S'", "S'": "S", "S2": "S2"}

class CubeGenome:
    def __init__(self, genome=None):
        if genome is None:
            self.genome = random.choices(all_possible_moves, k=random.randint(10, 20))
        else:
            self.genome = genome

    def fitness(self, start_state, desired_end_state):
        start_cube = magiccube.Cube(3, start_state)
        score = 0
        for i, move in enumerate(self.genome):
            start_cube.rotate(move)
            if get_cube_state(start_cube) == desired_end_state:
                # print(f"End state occured at move {i} of {self.genome}")
                self.genome = self.genome[:i+1]
                return score + 500

        # Subtract from the score the number of locations in which the cubes differ, but reward for where they are equal
        end_result = get_cube_state(start_cube)
        for end_state_char, end_result_char in zip(desired_end_state, end_result):
            if end_state_char != end_result_char:
                score -= 5
            else:
                score += 1

        return score

    def crossover(self, other):
        crossover_point_self = random.randint(0, len(self.genome) - 1)
        crossover_point_other = random.randint(0, len(other.genome) - 1)
        return CubeGenome(self.genome[:crossover_point_self] + other.genome[crossover_point_other:])

    def mutate(self):
        mutation_types = ["single_move_mutation", "reversal_of_a_move", "reversal_of_a_group_of_moves", "randomly_insert_a_move", "duplicate_a_group_of_moves", "randomly_remove_a_move", "randomly_remove_a_group_of_moves", "randomly_swap_two_moves", "randomly_swap_two_groups_of_moves"]
        mutation_type = random.choice(mutation_types)
        if mutation_type == "single_move_mutation":
            mutation_point = random.randint(0, len(self.genome) - 1)
            self.genome = self.genome[:mutation_point] + [random.choice(all_possible_moves)] + self.genome[mutation_point+1:]
        elif mutation_type == "reversal_of_a_move":
            mutation_point = random.randint(0, len(self.genome) - 1)
            self.genome = self.genome[:mutation_point] + [move_reversals[self.genome[mutation_point]]] + self.genome[mutation_point+1:]
        elif mutation_type == "reversal_of_a_group_of_moves":
            group_start = random.randint(0, len(self.genome) - 1)
            group_end = random.randint(group_start, len(self.genome) - 1)
            self.genome = self.genome[:group_start] + self.genome[group_start:group_end][::-1] + self.genome[group_end:]
        elif mutation_type == "randomly_insert_a_move":
            insertion_point = random.randint(0, len(self.genome) - 1)
            self.genome = self.genome[:insertion_point] + [random.choice(all_possible_moves)] + self.genome[insertion_point:]
        elif mutation_type == "duplicate_a_group_of_moves":
            group_start = random.randint(0, len(self.genome) - 1)
            group_end = random.randint(group_start, len(self.genome) - 1)
            self.genome = self.genome[:group_start] + self.genome[group_start:group_end] + self.genome[group_end:]
        elif mutation_type == "randomly_remove_a_move":
            self.genome = self.genome[:random.randint(0, len(self.genome) - 1)] + self.genome[random.randint(0, len(self.genome) - 1)+1:]
        elif mutation_type == "randomly_remove_a_group_of_moves":
            group_start = random.randint(0, len(self.genome) - 1)
            group_end = random.randint(group_start, len(self.genome) - 1)
            self.genome = self.genome[:group_start] + self.genome[group_end:]
        elif mutation_type == "randomly_swap_two_moves":
            swap_point_1 = random.randint(0, len(self.genome) - 1)
            swap_point_2 = random.randint(0, len(self.genome) - 1)
            self.genome = self.genome[:swap_point_1] + [self.genome[swap_point_2]] + self.genome[swap_point_1+1:swap_point_2] + [self.genome[swap_point_1]] + self.genome[swap_point_2+1:]
        elif mutation_type == "randomly_swap_two_groups_of_moves":
            group_start_1 = random.randint(0, len(self.genome) - 1)
            group_end_1 = random.randint(group_start_1, len(self.genome) - 1)
            group_start_2 = random.randint(0, len(self.genome) - 1)
            group_end_2 = random.randint(group_start_2, len(self.genome) - 1)
            self.genome = self.genome[:group_start_1] + self.genome[group_start_2:group_end_2] + self.genome[group_start_1:group_end_1] + self.genome[group_end_2:]

    def __str__(self):
        return " ".join(self.genome)

    def __repr__(self):
        return self.__str__()

