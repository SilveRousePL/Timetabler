import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Report(metaclass=Singleton):
    def __init__(self):
        self.data = []
        self.starting_time = time.time()
        self.check_builder = None
        self.record('### REPORT ###\n')

    def start_timer(self):
        self.starting_time = time.time()

    def record_iteration(self, solution, iteration):
        hcsc = self.check_builder.build(solution).get_all_cost()
        self.record(f'I={iteration}\tT={(time.time()-self.starting_time):.3f}\t'
                    f'HC={hcsc[0]}\tSC={hcsc[1]}\tSum={hcsc[2]}')

    def record(self, text: str = '', end='\n'):
        self.data.append(f'{text}{end}')
        print(text, end=end)

    def save(self, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            for line in self.data:
                f.writelines(line)
