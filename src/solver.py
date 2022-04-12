from algorithms.sa_own import AnnealingOwn
from algorithms.sa_lib import AnnealingLib
from algorithms.ts_own import TabuSearchOwn
from context import Context
from report import Report


class Solver():
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.solution_builder = ctx.solution_builder
        self.checker_builder = ctx.checker_builder
        self.initial_solution = None

    def profile(self, func, *args, **kwargs):
        import cProfile
        import pstats
        import sys
        pr = cProfile.Profile()
        pr.enable()
        return_val = func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr, stream=sys.stdout)
        ps.print_stats()
        return return_val

    def run(self):
        best_solution = None
        best_solution_cost = 2**32
        best_iteration = 0
        solutions_cost = []
        valid_number = 0
        invalid_number = 0
        for i in range(self.ctx.cfg['iterations']):
            Report().record(f'Iteration {i+1}/{self.ctx.cfg["iterations"]}')
            Report().start_timer()
            solution = getattr(self, self.ctx.cfg['algorithm'])()  # Run algorithm (based on configuration)
            cost = self.checker_builder.build(solution).get_all_cost()
            solutions_cost.append(cost[2])
            if cost[0] == 0:
                valid_number += 1
            else:
                invalid_number += 1

            if cost[2] < best_solution_cost:
                best_solution = solution
                best_solution_cost = cost[2]
                best_iteration = i+1
                Report().record('NEW BEST SOLUTION!')
            Report().record('-------------------')

        Report().record('===================')
        Report().record('# RESULTS #')
        Report().record(f'Valid solutions: {valid_number}')
        Report().record(f'Invalid solutions: {invalid_number}')
        Report().record(f'Average cost: {sum(solutions_cost)/len(solutions_cost)}')
        Report().record(f'Best iteration: {best_iteration}')
        self.ctx.set_solution(best_solution)
        self.ctx.save_solution()

    def sa_own(self, initial_solution=None):
        Report().record('Algorithm: Simulated Annealing (Own)')
        Report().record('Parameters: ')
        for k, v in self.ctx.cfg['sa_own'].items():
            Report().record(f'\t{k}={v}')
        Report().record()
        algorithm = AnnealingOwn(self.solution_builder,
                                 self.checker_builder)
        t_start = self.ctx.cfg['sa_own']['t_start']
        t_change_factor = self.ctx.cfg['sa_own']['t_change_factor']
        worse_acceptable = self.ctx.cfg['sa_own']['worse_acceptable']
        state = algorithm.run(t_start, t_change_factor, worse_acceptable)
        return state

    def sa_lib(self, initial_solution=None):
        Report().record('Algorithm: Simulated Annealing (Lib)')
        Report().record('Parameters: ')
        for k, v in self.ctx.cfg['sa_lib'].items():
            Report().record(f'\t{k}={v}')
        Report().record()
        algorithm = AnnealingLib(self.solution_builder,
                                 self.checker_builder)
        algorithm.Tmax = self.ctx.cfg['sa_lib']['Tmax']  # Max (starting) temperature
        algorithm.Tmin = self.ctx.cfg['sa_lib']['Tmin']  # Min (ending) temperature
        algorithm.steps = self.ctx.cfg['sa_lib']['steps']  # Number of iterations
        algorithm.updates = self.ctx.cfg['sa_lib']['updates']  # Number of updates
        algorithm.copy_strategy = self.ctx.cfg['sa_lib']['copy_strategy']
        state_list, e = algorithm.anneal()
        state = self.solution_builder.build(state_list)
        return state

    def ts_own(self, initial_solution=None):
        Report().record('Algorithm: Tabu Search (Own)')
        Report().record('Parameters: ')
        for k, v in self.ctx.cfg['ts_own'].items():
            Report().record(f'\t{k}={v}')
        Report().record()
        max_tabu_size = self.ctx.cfg['ts_own']['max_tabu_size']
        limit = self.ctx.cfg['ts_own']['limit']
        no_better_max_iter = self.ctx.cfg['ts_own']['no_better_max_iter']
        algorithm = TabuSearchOwn(self.solution_builder,
                                  self.checker_builder)
        state = algorithm.run(max_tabu_size, limit, no_better_max_iter)
        return state
