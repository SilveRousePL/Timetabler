from itertools import count
from datetime import datetime
import json

datetime_format = '%H:%M'


class Timeslot(object):
    _ids = count(0)

    def __init__(self, time: str, day: str):
        self.id = next(self._ids)
        self.datetime = datetime.strptime(time, datetime_format)
        self.day = day

    def __str__(self):
        return f'{self.day} {self.time()}'

    def __eq__(self, other):
        if isinstance(other, Timeslot):
            return (self.datetime == other.datetime
                    and self.day == other.day)
        return self == other

    def time(self):
        return self.datetime.strftime(datetime_format)

    def day(self):
        return self.day


class Room(object):
    _ids = count(0)

    def __init__(self, name: str, type: str):
        self.id = next(self._ids)
        self.name = name
        self.type = type

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Room):
            return self.name == other.name
        return self == other


class Teacher(object):
    _ids = count(0)

    def __init__(self, name: str):
        self.id = next(self._ids)
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Teacher):
            return self.name == other.name
        return self == other


class Course(object):
    _ids = count(0)

    def __init__(self, subject: str, room_type: str, teacher: str,
                 amount: int):
        self.id = next(self._ids)
        self.subject = subject
        self.room_type = room_type
        self.teacher = teacher
        self.amount = amount

    def __str__(self):
        return f'C[{self.subject}, {self.room_type}, {self.teacher}, \
                  {self.amount}]'

    def __eq__(self, other):
        if isinstance(other, Course):
            return self.id == other.id
        return self == other


class Group(object):
    _ids = count(0)

    def __init__(self, name: str, courses: 'list[Course]'):
        self.id = next(self._ids)
        self.name = name
        self.courses = courses

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Group):
            return self.name == other.name
        return self == other


class InputData(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.timeslots = []
        self.timeslots_per_day = {}
        self.rooms = []
        self.rooms_per_type = {}
        self.teachers = []
        self.groups = []
        self.init()

    def load(self, filename: str):
        with open(filename) as f:
            return json.load(f)

    def init(self):
        d = self.load(self.filename)

        # Create timeslots
        for timeslot_day, timeslots_list in d['timeslots'].items():
            for timeslot in timeslots_list:
                self.timeslots.append(Timeslot(timeslot, timeslot_day))

        # Create timeslots per day
        for timeslot_day, timeslots_list in d['timeslots'].items():
            self.timeslots_per_day[timeslot_day] = []
            for timeslot in timeslots_list:
                self.timeslots_per_day[timeslot_day].append(
                    Timeslot(timeslot, timeslot_day))

        # Create rooms
        for room_type, rooms_list in d['rooms'].items():
            for room_name in rooms_list:
                self.rooms.append(Room(room_name, room_type))

        # Create rooms per type
        for room_type, rooms_list in d['rooms'].items():
            self.rooms_per_type[room_type] = []
            for room in rooms_list:
                self.rooms_per_type[room_type].append(
                    Room(room, room_type))

        # Create teachers
        for teacher in d['teachers']:
            self.teachers.append(Teacher(teacher))

        # Create groups
        for group in d['groups']:
            courses = []
            for course in group['courses']:
                subject = course['subject']
                room_type = course['room']
                teacher = course['teacher']
                amount = course['amount']
                courses.append(Course(subject, room_type, teacher, amount))
            self.groups.append(Group(group['name'], courses))
