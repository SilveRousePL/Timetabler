from itertools import count
from input import Group


class Puzzle(object):
    _ids = count(1)

    def __init__(self, group_name: str, subject: str,
                 teacher: str, room_type: str):
        self.id = next(self._ids)
        self.group_name = group_name
        self.subject = subject
        self.teacher = teacher
        self.room_type = room_type

    def __int__(self):
        return self.id

    def __float__(self):
        return float(self.id)

    def __str__(self):
        return (
            f'LP{self.id}[{self.group_name}, {self.subject}, '
            f'{self.teacher}, {self.room_type}]'
        )

    def __eq__(self, other):
        if isinstance(other, Puzzle):
            return self.id == other.id
        if isinstance(other, Empty):
            return False
        if other is None:
            return False
        return self == other


class Empty(object):
    _ids = count(1)

    def __init__(self):
        self.id = -next(self._ids)

    def __int__(self):
        return self.id

    def __float__(self):
        return float(self.id)

    def __str__(self):
        return '-E-'

    def __eq__(self, other):
        if isinstance(other, Empty):
            return self.id == other.id
        if isinstance(other, Puzzle):
            return False
        if other is None:
            return True
        return self == other


class Puzzler():
    def __init__(self, groups: 'list[Group]'):
        self.data = self.__build(groups)

    def __getitem__(self, id):
        return self.data[id]

    def __len__(self):
        return len(self.data)

    def __build(self, groups: 'list[Group]'):
        result = []
        for group in groups:
            for course in group.courses:
                for i in range(course.amount):
                    result.append(
                        Puzzle(group.name, course.subject,
                               course.teacher, course.room_type)
                    )
        return result
