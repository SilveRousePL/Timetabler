import random
from puzzler import Empty


class Solution(object):
    def __init__(self, data: list, timeslots: list, rooms: list):
        self.data = data
        self.timeslots = timeslots
        self.rooms = rooms

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        if isinstance(other, Solution):
            return self.data == other.data
        return self == other

    def __hash__(self):
        return hash(str(self.data))

    def matrix(self):
        def chunk_it(seq, num):
            avg = len(seq) / float(num)
            out = []
            last = 0.0
            while last < len(seq):
                out.append(seq[int(last):int(last + avg)])
                last += avg
            return out

        divider = len(self.data) / len(self.timeslots)
        result = chunk_it(self.data, divider)
        return result

    def matrix_tr(self):
        return [list(i) for i in zip(*self.matrix())]


class SolutionBuilder():
    def __init__(self, puzzles: list, timeslots, rooms):
        self.puzzles = puzzles
        self.timeslots = timeslots
        self.rooms = rooms
        self.empties = self.__gen_empties()

    def build(self, solution_list: list):
        return Solution(solution_list, self.timeslots, self.rooms)

    def copy(self, solution: Solution):
        solution_data = solution.data[:]  # copying by slicing
        return self.build(solution_data)

    def build_from_ids(self, solution_list_ids: list):
        solution_list = []
        for i in solution_list_ids:
            if i >= 0:
                solution_list.append(self.puzzles[int(i)])
            else:
                solution_list.append(self.empties[int(i)])
        return Solution(solution_list, self.timeslots, self.rooms)

    def replace_with_puzzle_solution(self, solution: Solution):
        matrix = solution.matrix()
        for i in matrix:
            for j in i:
                if isinstance(j, Empty):
                    continue
                j = self.puzzles[j]
        return matrix

    def random_solution(self):
        # Filling lists with LPs
        solution = []
        for lp in self.puzzles.data:
            solution.append(lp)

        # Filling up free slots
        for empty in self.empties:
            solution.append(empty)

        # Shuffle the contents of the lists
        random.shuffle(solution)
        return self.build(solution)

    def __gen_empties(self):
        result = []
        amount = len(self.timeslots) * len(self.rooms) - len(self.puzzles)
        if amount:
            for _ in range(amount):
                result.append(Empty())
        return result
