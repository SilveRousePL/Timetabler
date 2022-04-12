import os
import json
import input
import output
from report import Report
from solution import Solution, SolutionBuilder
from checker import CheckerBuilder
from puzzler import Empty, Puzzler


class Context:
    def __init__(self, config_file):
        # Initialize context
        self.cfg = self.load_config(config_file)

        # JSON input data
        self.input = input.InputData(self.cfg['input_file'])
        # REPORT #
        Report().record(f'Input filename: {self.cfg["input_file"]}')
        Report().record(f'Number of days: {len(self.input.timeslots_per_day)}')
        Report().record(f'Number of timeslots: {len(self.input.timeslots)}')
        Report().record(f'Number of rooms: {len(self.input.rooms)}')
        Report().record(f'Number of teachers: {len(self.input.teachers)}')
        Report().record(f'Number of groups: {len(self.input.groups)}', end='\n\n')
        Report().record(f'Problem size: n={len(self.input.timeslots)*len(self.input.rooms)}', end='\n\n')

        # Matrix rows and columns
        self.timeslots = self.input.timeslots
        self.rooms = self.input.rooms

        # Create puzzles and solution/checker builder
        self.lesson_puzzles = Puzzler(self.input.groups)
        self.solution_builder = SolutionBuilder(self.lesson_puzzles,
                                                self.timeslots, self.rooms)
        self.checker_builder = CheckerBuilder(self.input, self.lesson_puzzles)
        # REPORT #
        Report().check_builder = self.checker_builder
        occupied = len(self.lesson_puzzles.data)
        total = len(self.timeslots) * len(self.rooms)
        percent = occupied / total * 100
        Report().record(f'Number of occupied slots: {occupied}')
        Report().record(f'Total number of slots: {total}')
        Report().record(f'This is {percent}% of all slots ', end='\n\n')

        # Results are stored here
        self.best_solution = None
        self.best_matrix = None
        self.best_matrix_tr = None
        self.best_matrix_lps = None
        self.best_matrix_lps_tr = None
        self.best_cost = None

        # Lessons list
        self.lessons = []

    def load_config(self, filename):
        with open(filename) as f:
            return json.load(f)

    def set_solution(self, solution):
        if isinstance(solution, Solution):
            self.best_solution = solution
        else:
            self.best_solution = self.solution_builder.build(solution)
        self.best_matrix = self.best_solution.matrix()
        self.best_matrix_tr = [list(i) for i in zip(*self.best_matrix)]
        check = self.checker_builder.build(self.best_solution)
        self.best_cost = check.get_cost()

        # Generate best matrix with lesson puzzles
        self.best_matrix_lps = []
        for rlist in self.best_matrix:
            room_result = []
            for lp in rlist:
                room_result.append(lp)
            self.best_matrix_lps.append(room_result)

        self.best_matrix_lps_tr = [list(i) for i in zip(*self.best_matrix_lps)]

        # Generate lesson list
        for room, rlist in zip(self.rooms, self.best_matrix_lps):
            for time, puzzle in zip(self.timeslots, rlist):
                if isinstance(puzzle, Empty):
                    continue
                self.lessons.append(
                    output.Lesson(
                        puzzle.group_name,
                        str(time),
                        puzzle.subject,
                        puzzle.teacher,
                        str(room)
                    ))

        # REPORT
        Report().record('--- BEST SOLUTION ---')
        Report().record(f'RESULT: {check.get_summary_cost()}')
        Report().record(f'Number of hard conflicts: {self.best_cost[0]}')
        Report().record(f'Number of soft conflicts: {self.best_cost[1]}')
        if self.best_cost[0] == 0:
            Report().record('The solution is correct!')
        else:
            Report().record('The solution is NOT correct!')

    def save_solution(self):
        os.makedirs(os.path.dirname(self.cfg['output_file_json']), exist_ok=True)
        self.json_out = output.OutputJSON(self.cfg['output_file_json'],
                                          self.lessons)
        self.json_out.save()
        os.makedirs(os.path.dirname(self.cfg['output_file_csv']), exist_ok=True)
        self.csv_out = output.OutputCSV(self.cfg['output_file_csv'],
                                        self.lessons)
        self.csv_out.save()
        os.makedirs(os.path.dirname(self.cfg['output_dir_tables']), exist_ok=True)
        self.tables_out = output.OutputTables(self.cfg['output_dir_tables'],
                                              self.input.timeslots_per_day,
                                              self.lessons)
        self.tables_out.save()
        Report().record()
        Report().save(self.cfg['output_report'])
