from solution import Solution
from puzzler import Empty
import itertools


class Checker():
    def __init__(self, solution: Solution, input, puzzles):
        self.solution = solution
        self.input = input
        self.lps = puzzles
        self.matrix = solution.matrix()
        self.matrix_tr = [list(i) for i in zip(*self.matrix)]

    def get_cost(self):
        hard = self.__calc_hard_constraints()
        soft = self.__calc_soft_constraints()
        return (hard, soft)

    def get_summary_cost(self):
        hard = self.__calc_hard_constraints()
        soft = self.__calc_soft_constraints()
        return hard * 100 + soft

    def get_all_cost(self):
        hard = self.__calc_hard_constraints()
        soft = self.__calc_soft_constraints()
        return (hard, soft, hard * 100 + soft)

    def __calc_hard_constraints(self):
        conflicts_amount = 0
        # Do we have multiple use of a limited resource?
        conflicts_amount += self.__no_multi_use_limited_resource_constraint()
        # Do we have free periods between lessons for groups?
        conflicts_amount += self.__no_free_periods_for_groups_constraint()
        # Do we have badly chosen rooms?
        conflicts_amount += self.__badly_chosen_rooms_constraint()
        return conflicts_amount

    def __calc_soft_constraints(self):
        conflicts_amount = 0
        # Do we have many passages between rooms?
        conflicts_amount += self.__no_many_passages_between_rooms_constraint()
        # Do we have the same number of lessons every day?
        conflicts_amount += self.__the_same_number_of_lessons_every_day_constraint()
        return conflicts_amount

    # Do we have multiple use of a limited resource?
    def __no_multi_use_limited_resource_constraint(self):
        result = 0
        for timeslot_list in self.matrix_tr:
            # Does the teacher only have one lesson at a time?
            teachers = [o.teacher for o in timeslot_list
                        if not isinstance(o, Empty)]
            # Does the group only have one lesson at a time?
            groups = [o.group_name for o in timeslot_list
                      if not isinstance(o, Empty)]
            result += self.__count_duplicates(teachers)
            result += self.__count_duplicates(groups)
        return result

    # Do we have free periods between lessons for groups?
    def __no_free_periods_for_groups_constraint(self):
        result = 0
        days = {}
        for timeslot, timeslot_list in zip(
                                        self.input.timeslots, self.matrix_tr):
            groups_in_timeslot = [o.group_name for o in timeslot_list
                                  if not isinstance(o, Empty)]
            if timeslot.day not in days:
                days[timeslot.day] = []
            days[timeslot.day].append(groups_in_timeslot)

        all_groups = self.input.groups
        for day in days.values():
            for group in all_groups:
                presence = []
                for timeslot_list in day:
                    if group.name in timeslot_list:
                        presence.append(True)
                    else:
                        presence.append(False)

                if True not in presence:
                    continue
                first_index = presence.index(True)
                last_index = len(presence) - presence[::-1].index(True)

                presence = presence[first_index:last_index]
                result += presence.count(False)

        return result

    # Do we have badly chosen rooms?
    def __badly_chosen_rooms_constraint(self):
        result = 0
        for room_name, room_list in zip(self.input.rooms, self.matrix):
            room_type = [x for x in self.input.rooms_per_type.keys()
                         if room_name in self.input.rooms_per_type[x]][0]
            for lp in room_list:
                if isinstance(lp, Empty):
                    continue
                if lp.room_type != room_type:
                    result += 1
        return result

    # Do we have many passages between rooms?
    def __no_many_passages_between_rooms_constraint(self):
        result = 0
        for room_list in self.matrix:
            groups = [o.group_name
                      for o in room_list if not isinstance(o, Empty)]
            cycle1 = itertools.cycle(groups)
            cycle2 = itertools.cycle(groups)
            next(cycle2)
            for i in range(len(groups)):
                curr_element = next(cycle1)
                next_element = next(cycle2)
                if curr_element != next_element:
                    result += 1
        return result

    # Do we have the same number of lessons every day?
    def __the_same_number_of_lessons_every_day_constraint(self):
        result = 0
        days = {}
        for timeslot, timeslot_list in zip(
                                        self.input.timeslots, self.matrix_tr):
            groups_in_timeslot = [o.group_name for o in timeslot_list
                                  if not isinstance(o, Empty)]
            if timeslot.day not in days:
                days[timeslot.day] = []
            days[timeslot.day].append(groups_in_timeslot)

        all_groups = self.input.groups
        for group in all_groups:
            number_of_lessons_per_day = []
            for day in days.values():
                lessons_number = 0
                for timeslot_list in day:
                    if group.name in timeslot_list:
                        lessons_number += 1
                number_of_lessons_per_day.append(lessons_number)
            result += (max(number_of_lessons_per_day) - min(number_of_lessons_per_day))

        return result

    def __count_duplicates(self, lst):
        lwd = list(dict.fromkeys(lst))
        return len(lst) - len(lwd)


class CheckerBuilder():
    def __init__(self, input, puzzles):
        self.input = input
        self.puzzles = puzzles

    def build(self, solution: Solution):
        return Checker(solution, self.input, self.puzzles)
