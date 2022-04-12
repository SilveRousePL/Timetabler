# Timetabler
Project created as the research environment for a master's thesis.

Master's thesis name: _Comparative analysis of algorithms for arranging teaching plans_

![](https://github.com/SilveRousePL/Timetabler/blob/master/about.gif)

---
## First usage
_**Tip**: Check chmod if you are unable to run the scripts below :)_
1. Install dependencies:
```shell
./venv_install.sh
```
2. Let's try to run it:
```shell
./run.sh
```

---
## Input
The input of the application is the configuration file, which you'll find in `resources/config.json`. Example `config.json`:
```json
{
    // Input JSON file with parameters on the basis of which timetables are created
    "input_file":        "resources/test_sets/medium.json",
    // Output files in various forms and formats
    "output_file_json":  "resources/out/medium/sa_own/output.json",
    "output_file_csv":   "resources/out/medium/sa_own/output.csv",
    "output_dir_tables": "resources/out/medium/sa_own/output_tables/",
    "output_report":     "resources/out/medium/sa_own/report.txt",

    // The name of the algorithm to run. 
    // Should be like the method name in class Solver (solver.py)
    "algorithm": "sa_own",
    "iterations": 10,

    // Parameters for each algorithm that is run from a method with the same name
    "sa_own": {
        // ...
    },
    "sa_lib": {
        // ...
    },
    "ts_own": {
        // ...
    }
    // ...
}
```

## Timetable parameters:
Let's see what the sample JSON input file looks like with the parameters on the basis of which the timetable is built:
```json
{
    // Time slots available for lessons.
    "timeslots": {
        "Monday": ["08:00", "08:50", "09:45", ...],
        "Tuesday": ... ,
        ...
    },
    // Available classrooms for teaching purposes.
    // The key is a type of room. 
    // The value is a list of rooms (names). 
    "rooms": {
        "General": ["R101", "R102", "R103", ...],
        "IT": ["I301", "I302", ...],
        "Sport": ["S1"],
        ...
    },
    // Simple list of teachers
    "teachers": [
        "Mikołaj Wróblewski",
        "Lucjan Pietrzak",
        "Eliza Chmielewska",
        "Urszula Sokołowska",
        ...
    ],
    // List of study groups
    // Each group has its own name and the courses they attend
    "groups": [
        {
            "name": "IVa",
            // List of courses. 
            // Each course has its own name, type of room,
            // teacher, and the number of occurrences per week.
            "courses": [
                {
                    "subject": "Matematyka",
                    "room": "General",  // Room type
                    "teacher": "Mikołaj Wróblewski",
                    "amount": 5
                },
                {
                    "subject": "Informatyka",
                    "room": "IT",  // Room type
                    "teacher": "Lucjan Pietrzak",
                    "amount": 2
                },
                {
                    "subject": "WF",
                    "room": "Sport",  // Room type
                    "teacher": "Eliza Chmielewska",
                    "amount": 4
                },
                ...
            ]
        },
        {
            "name": "IVb",
            "courses": [
                ...
            ]
        },
        {
            "name": "Va",
            "courses": [
                ...
            ]
        },
        ...
    ]
}

```
Example test sets are located in `resources/test_sets` directory.

## Output
The output files are generated into several forms:
- List of lessons in CSV (comma-separated values) format
- List of lessons in JSON format
- Tables:
    - Tables for each group
    - Tables for each teacher
    - Summary table for groups
    - Summary table for teachers
- Report textfile

You can find examples in `resources/out` directory.

---
## Description of modules and classes

### Input/Output
The `Input` and `Output` modules are used to read and parse input data and generate and write output data. 
The `Input` module contains the main part responsible for parsing input JSON files and also contains class implementations whose instances are created at parsing time. Objects created during parsing include:
- Timeslot
- Room
- Teacher
- Group
- Course

The `Group` class contains, in addition to the name of the occupational group, information about the courses taught to that group.
Class `Course` describes the full course of the subject, who teaches it, what kind of classroom is needed for this course and the number of lessons of this course in one period.
It is worth noting that it is possible to define a specific teacher for a subject, who will teach this class, and the classroom can be chosen arbitrarily from free classrooms of the given type.
The `Output` module contains the main part responsible for processing the solutions to the list of classes and generating the output to the appropriate formats i.e. schedules for groups, schedules for teachers and summary schedules. The whole module of writing to output formats is based on a list of lessons, which was generated from an object of type `Solution`. 
The lesson here is described by the `Lesson` class, which describes what class the lesson is for, when it is, what subject it is in, who will teach the lesson, and where it will take place.

### Context
The `Context` module stores all object instances created to solve the current problem. It creates and provides instances for reading configurations, reading test suites, creates instances of object factories i.e. `Puzzle`, `Solution` and `Checker` and provides helper methods to save the best solution.

### Puzzler
The `Puzzler` module contains a factory of objects of type `Puzzle`, makes them available and has a description of the `Puzzle` object. The `Puzzle` object stores information similar to the `Lesson` object except that it does not contain fields for time slot and classroom. Additionally, it contains a field describing the type of classroom. The `Puzzle` objects are single units that are arranged in a two-dimensional matrix, which then creates a solution with them.

### Solution
The `Solution` module contains an implementation of the `Solution` class, which is an object that represents a solution. It consists of a list in which objects of type `Puzzle` are arranged, it has a list of time slots which here are treated as row descriptions of the matrix, and it has a list of classrooms which are column headers.
The `Solution` object also has methods that convert the current list of `Puzzle` objects into objects of real ordinary matrices, transposed matrices, and allows to generate a list of identification numbers of Puzzle objects in case the algorithm under study cannot process a list of objects other than the numeric type. 
The module also includes a solution factory `SolutionBuilder`, which has methods to build, generate, and copy instances of the `Solution` class and makes them easy to manage.

### Checker
The `Checker` module contains an implementation of the `Checker` class, which is an object that evaluates a solution based on its satisfaction of a number of constraints. An instance of the `Checker` class contains access to the input data and is created by the `CheckerBuilder` factory, which contains a method to create an instance based on the solution provided in the parameter.
The created `Checker` object has two methods that return the criterion value for the solution. The first method gives the result as a pair of integers, the first of which is the number of conflicts for hard constraints, while the second is the number of conflicts for soft constraints.
The second method returns a single integer (criterion value), which is calculated based on the formula: $R = 100 * R_{HC} + R_{SC}$, where $R_{HC}$ is the number of conflicts for hard constraints and $R_{SC}$ is the number of conflicts for soft constraints.
Methods that return the number of conflicts first call other private methods, which are implementations that count the number of occurrences of conflicts. The classification of which method to treat as a hard or soft constraint was achieved by creating two intermediary methods that act as checklists of method calls. Both methods work identically, but are treated separately in the output as methods for computing hard and soft constraints.

### Solver
In the `Solver` module, the only implementation is the `Solver` class and it is used to run the actual algorithm or set of algorithms and when the algorithm(s) have completed, it writes the returned solution to the `Context` object. The `Solver` class has private method calls that implement the correct ways to initialize and run each algorithm. Selecting the correct algorithms to test is accomplished by changing the values in the configuration file.

---
## Implemented Constraints
Constraints are implemented in the `Checker` module. This module was created in such a way that further constraint implementations can be added and assigned to hard or soft constraints in an accessible and transparent way. The constraints used in the current implementation are very basic and can often be found in school lesson plans.
### Hard constraints
- **Avoiding repeated use of a constrained resource**
    
    Resources such as teachers, class groups, or rooms cannot be used multiple times at the same time and this must be avoided for the schedule to be considered feasible. It is worth noting that the solution structure technically blocks the use of the same classroom in a single time slot, so redundant checking of this constraint is not needed.
- **Avoiding free slots for lesson groups**
    
    Lessons for a class group on a given day must run in a single sequence, and there cannot be a free time slot between lessons.
- **Avoid using the wrong type of classroom for the type of lesson**

    Specific subjects must be held in classrooms suitable for such classes. For example: physical education or computer science must be held in a room suitable for such classes.

### Soft constraints
- **Avoiding too many transitions between classrooms**

    If a class group has multiple lessons that can be held in one type of classroom then we try to avoid moving such a group unnecessarily.
- **Even distribution of lessons on each day**

    Lessons for a class group should take about the same amount of time each day. We try to avoid having one day completely full and another day empty or nearly empty.

---
## Ideas
- GUI for building input data and display output
- More efficient algorithms to finding solutions (See how the other algorithms are attached and connect yours in the same way in the `solver.py` file).
- More hard and soft constraints
- Refactoring and application optimalization
