#!/usr/bin/python3

from context import Context
from solver import Solver


cfg_file = 'resources/config.json'


def main(ctx: Context):
    solver = Solver(ctx)
    solver.run()


if __name__ == "__main__":
    ctx = Context(cfg_file)
    main(ctx)
