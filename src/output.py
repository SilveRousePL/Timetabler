from itertools import count
from tabulate import tabulate
import jsonpickle


class Lesson(object):
    _ids = count(0)

    def __init__(self, group_name: str, timeslot: str, subject: str,
                 teacher: str, room: str):
        self.id = next(self._ids)
        self.group = group_name
        self.timeslot = timeslot
        self.subject = subject
        self.teacher = teacher
        self.room = room

    def __str__(self):
        return (
            f'{self.group}, {self.timeslot}, {self.subject}, '
            f'{self.teacher}, {self.room}'
        )

    def __eq__(self, other):
        if isinstance(other, Lesson):
            return self.id == other.id
        return self == other


class OutputTables(object):
    def __init__(self, dir_name: str,
                 timeslots_per_day, lessons):
        self.dir_name = dir_name
        self.timeslots_per_day = timeslots_per_day
        self.lessons = lessons

    def save(self):
        self.__save_groups()
        self.__save_teachers()
        self.__save_groups_summary()
        self.__save_teachers_summary()

    def __save_groups(self):
        lessons_by_group = {}
        for lesson in self.lessons:
            if lesson.group not in lessons_by_group:
                lessons_by_group[lesson.group] = []
            lessons_by_group[lesson.group].append(lesson)

        for group, lessons in lessons_by_group.items():
            group_result_headers = []
            group_result_table = []

            group_result_headers.append('Time')
            group_result_table.append([])
            for time in self.timeslots_per_day['Monday']:
                group_result_table[-1].append(time.time())

            for day, time_list in self.timeslots_per_day.items():
                group_result_headers.append(day)
                group_result_table.append([])
                for time in time_list:
                    lesson = next(
                        (x for x in self.lessons
                            if x.timeslot == str(time) and x.group == group),
                        None)
                    if lesson is None:
                        group_result_table[-1].append('----')
                    else:
                        group_result_table[-1].append(
                            f'{lesson.subject}, {lesson.teacher}, Room {lesson.room}')

            group_result_table = [list(i) for i in zip(*group_result_table)]

            filename = f'{self.dir_name}/group_{group}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'TIMETABLE\nGroup {group}\n\n')
                f.write(tabulate(group_result_table,
                                 headers=group_result_headers))
                f.write('\n\n')

    def __save_teachers(self):
        lessons_by_teacher = {}
        for lesson in self.lessons:
            if lesson.teacher not in lessons_by_teacher:
                lessons_by_teacher[lesson.teacher] = []
            lessons_by_teacher[lesson.teacher].append(lesson)

        for teacher, lessons in lessons_by_teacher.items():
            teacher_result_headers = []
            teacher_result_table = []

            teacher_result_headers.append('Time')
            teacher_result_table.append([])
            for time in self.timeslots_per_day['Monday']:
                teacher_result_table[-1].append(time.time())

            for day, time_list in self.timeslots_per_day.items():
                teacher_result_headers.append(day)
                teacher_result_table.append([])
                for time in time_list:
                    lesson = next(
                        (x for x in self.lessons
                            if x.timeslot == str(time) and x.teacher == teacher),
                        None)
                    if lesson is None:
                        teacher_result_table[-1].append('----')
                    else:
                        teacher_result_table[-1].append(
                            f'{lesson.group}, {lesson.subject}, Room {lesson.room}')

            teacher_result_table = [list(i) for i in zip(*teacher_result_table)]

            filename = f'{self.dir_name}/teacher_{teacher}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'TIMETABLE\nTeacher {teacher}\n\n')
                f.write(tabulate(teacher_result_table,
                                 headers=teacher_result_headers))
                f.write('\n\n')

    def __save_groups_summary(self):
        lessons_by_group = {}
        for lesson in self.lessons:
            if lesson.group not in lessons_by_group:
                lessons_by_group[lesson.group] = []
            lessons_by_group[lesson.group].append(lesson)

        groups_result_headers = []
        groups_result_table = []
        groups_result_headers.append('Day Time')
        groups_result_table.append([])
        for day, times in self.timeslots_per_day.items():
            for time in times:
                groups_result_table[-1].append(str(time))

        for group, lessons in lessons_by_group.items():
            groups_result_headers.append(group)
            groups_result_table.append([])
            for day, time_list in self.timeslots_per_day.items():
                for time in time_list:
                    lesson = next((x for x in lessons if x.timeslot == str(time)), None)
                    if lesson is None:
                        groups_result_table[-1].append('----')
                    else:
                        groups_result_table[-1].append(
                            f'{lesson.subject}, {lesson.teacher}, {lesson.room}')

        groups_result_table = [list(i) for i in zip(*groups_result_table)]

        filename = f'{self.dir_name}/groups_summary.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('TOTAL PLAN FOR GROUPS \n\n')
            f.write(tabulate(groups_result_table,
                             headers=groups_result_headers))
            f.write('\n\n')

    def __save_teachers_summary(self):
        lessons_by_teacher = {}
        for lesson in self.lessons:
            if lesson.teacher not in lessons_by_teacher:
                lessons_by_teacher[lesson.teacher] = []
            lessons_by_teacher[lesson.teacher].append(lesson)

        teachers_result_headers = []
        teachers_result_table = []
        teachers_result_headers.append('Day Time')
        teachers_result_table.append([])
        for day, times in self.timeslots_per_day.items():
            for time in times:
                teachers_result_table[-1].append(str(time))

        for teacher, lessons in lessons_by_teacher.items():
            teachers_result_headers.append(teacher)
            teachers_result_table.append([])
            for day, time_list in self.timeslots_per_day.items():
                for time in time_list:
                    lesson = next((x for x in lessons if x.timeslot == str(time)), None)
                    if lesson is None:
                        teachers_result_table[-1].append('----')
                    else:
                        teachers_result_table[-1].append(
                            f'{lesson.group}, {lesson.subject}, {lesson.room}')

        teachers_result_table = [list(i) for i in zip(*teachers_result_table)]

        filename = f'{self.dir_name}/teachers_summary.txt'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('TOTAL PLAN FOR TEACHERS \n\n')
            f.write(tabulate(teachers_result_table,
                             headers=teachers_result_headers))
            f.write('\n\n')


class OutputJSON(object):
    def __init__(self, filename: str, lessons: list):
        self.filename = filename
        self.lessons = lessons

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            jsonpickle.set_encoder_options('json', ensure_ascii=False,
                                           indent=4)
            json_str = jsonpickle.encode(self.lessons, unpicklable=False)
            f.write(json_str)


class OutputCSV(object):
    def __init__(self, filename: str, lessons: list):
        self.filename = filename
        self.lessons = lessons

    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            for lesson in self.lessons:
                f.writelines(f'{str(lesson)},\n')
