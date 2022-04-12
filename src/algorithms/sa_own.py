import math
import random
from puzzler import Empty
from report import Report


class AnnealingOwn():
    def __init__(self, sol_builder, check_builder):
        self.sol_builder = sol_builder
        self.check_builder = check_builder
        self.iterator = 0  # REPORT

    def run(self, t_start, t_change_factor, worse_acceptable):
        return self.__optimize(t_start, t_change_factor, worse_acceptable)

    def __optimize(self, temperature,
                   temperature_change_factor, worse_acceptable):
        worse_solution_counter = 0

        current_solution = self.sol_builder.random_solution()
        best_solution = current_solution
        adjacent_solution = current_solution

        current_solution_cost = self.__fitness(current_solution)
        best_solution_cost = current_solution_cost
        adjacent_solution_cost = current_solution_cost

        while worse_solution_counter < worse_acceptable:
            self.iterator += 1  # REPORT
            adjacent_solution = self.__create_neighbor_solution(
                                current_solution)
            adjacent_solution_cost = self.__fitness(adjacent_solution)

            if adjacent_solution_cost < best_solution_cost:
                best_solution = adjacent_solution
                best_solution_cost = adjacent_solution_cost
                Report().record_iteration(best_solution, self.iterator)  # REPORT

            if adjacent_solution_cost < current_solution_cost:
                current_solution = adjacent_solution
                current_solution_cost = adjacent_solution_cost
                worse_solution_counter = 0
            else:
                worse_solution_counter += 1
                delta = adjacent_solution_cost - current_solution_cost
                x = random.random()
                if x < (math.exp(-delta / temperature)):
                    current_solution = adjacent_solution
                    current_solution_cost = adjacent_solution_cost

            temperature *= temperature_change_factor

        return best_solution

    def __create_neighbor_solution(self, solution):
        a = random.randint(0, len(solution) - 1)
        b = random.randint(0, len(solution) - 1)
        while (isinstance(solution[a], Empty)
                and isinstance(solution[b], Empty)):
            b = random.randint(0, len(solution) - 1)
        new_solution = self.sol_builder.copy(solution)
        (new_solution[a],
         new_solution[b]) = (new_solution[b],
                             new_solution[a])
        return new_solution

    def __fitness(self, solution):
        check = self.check_builder.build(solution)
        return check.get_summary_cost()
