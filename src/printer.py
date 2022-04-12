from context import Context
from puzzler import Empty
from tabulate import tabulate


class Printer():
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def table(self):
        print(tabulate(self.ctx.best_matrix))

    def table_group(self):
        for timeslot in self.ctx.best_matrix_tr:
            for i in timeslot:
                if isinstance(i, Empty):
                    print('None', end='\t')
                else:
                    print(i.group_name, end='\t')
            print()

    def occupied_slots(self):
        occupied = len(self.ctx.lesson_puzzles.data)
        total = len(self.ctx.timeslots) * len(self.ctx.rooms)
        percent = occupied / total * 100
        print(f'Number of occupied slots: {occupied}')
        print(f'Total number of slots: {total}')
        print(f'This is {percent}% of all slots ')

    def costs(self):
        hard_cost = self.ctx.best_cost[0]
        soft_cost = self.ctx.best_cost[1]
        print(f'Number of hard conflicts: {hard_cost}')
        print(f'Number of soft conflicts: {soft_cost}')
        if hard_cost == 0:
            print('The solution is correct!')
        else:
            print('The solution is NOT correct!')

    def lesson_list(self):
        for lesson in self.ctx.lessons:
            print(f'L{lesson.id}[{str(lesson)}]')
