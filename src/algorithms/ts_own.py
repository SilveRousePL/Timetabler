import random
from puzzler import Empty
from report import Report


class TabuSearchOwn():
    def __init__(self, sol_builder, check_builder):
        self.sol_builder = sol_builder
        self.check_builder = check_builder
        self.iterator = 0  # REPORT

    def run(self, max_tabu_size, limit, no_better_max_iter):
        return self.__optimize(max_tabu_size, limit, no_better_max_iter)

    def __optimize(self, max_tabu_size, limit, no_better_max_iter):
        current_solution = self.sol_builder.random_solution()
        best_solution = current_solution
        neighbor_solution = current_solution
        best_neighbor_solution = current_solution

        current_solution_cost = self.__fitness(current_solution)
        best_solution_cost = current_solution_cost
        neighbor_solution_cost = current_solution_cost
        best_neighbor_solution_cost = current_solution_cost

        tabu_list = []
        prev_solutions = []
        prev_sol_counter = 0
        no_better_counter = 0
        while not no_better_counter > no_better_max_iter:
            self.iterator += 1  # REPORT
            neighbor_solution = self.__create_neighbor_solution(
                                current_solution)
            neighbor_solution_cost = self.__fitness(neighbor_solution)
            if neighbor_solution not in tabu_list:
                if neighbor_solution_cost < best_neighbor_solution_cost:
                    best_neighbor_solution = neighbor_solution
                    best_neighbor_solution_cost = neighbor_solution_cost

            current_solution = best_neighbor_solution
            current_solution_cost = best_neighbor_solution_cost

            if (best_neighbor_solution_cost < best_solution_cost):
                prev_solutions.append((best_solution, best_solution_cost))
                tabu_list.append(best_neighbor_solution)

                best_solution = best_neighbor_solution
                best_solution_cost = best_neighbor_solution_cost

                Report().record_iteration(best_solution, self.iterator)  # REPORT

                no_better_counter = 0
                prev_sol_counter = 0

            if len(tabu_list) > max_tabu_size:
                tabu_list.pop(0)

            if len(prev_solutions) > 100:
                prev_solutions.pop(0)

            if prev_sol_counter > limit:
                if prev_solutions:  # if prev_solutions is not empty
                    index = random.randint(0, len(prev_solutions) - 1)
                    current_solution = prev_solutions[index][0]
                    current_solution_cost = prev_solutions[index][1]
                prev_sol_counter = 0

            prev_sol_counter += 1
            no_better_counter += 1
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
