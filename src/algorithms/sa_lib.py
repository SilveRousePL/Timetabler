from simanneal import Annealer
from puzzler import Empty
import random
from report import Report


class AnnealingLib(Annealer):
    def __init__(self, sol_builder, check_builder):
        self.sol_builder = sol_builder
        self.check_builder = check_builder
        state = self.sol_builder.random_solution().data
        # REPORT
        self.last_best_energy = 2**32
        self.iterator = 0
        # END
        super(AnnealingLib, self).__init__(state)

    def move(self):
        initial_energy = self.energy()
        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        while (isinstance(self.state[a], Empty)
                and isinstance(self.state[b], Empty)):
            b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]
        # REPORT
        self.iterator += 1
        if self.best_energy < self.last_best_energy:
            best_solution = self.sol_builder.build(self.best_state)
            Report().record_iteration(best_solution, self.iterator)
            self.last_best_energy = self.best_energy
        # END
        return self.energy() - initial_energy

    def energy(self):
        solution = self.sol_builder.build(self.state)
        check = self.check_builder.build(solution)
        return check.get_summary_cost()
