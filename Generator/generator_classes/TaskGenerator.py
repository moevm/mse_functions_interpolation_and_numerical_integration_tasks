from numpy import random
from Tasks.InterpolationTask import InterpolationTask
from Tasks.SplineTask import SplineTask
from Tasks.Integration.SimpsonTask import SimpsonTask
from Tasks.Integration.TrapezoidTask import TrapezoidTask


class TaskGenerator:
    def __init__(self, structure, number_of_variants, seed=None):
        self.seed = seed if seed is not None else random.randint(0, 1000000)
        self.structure = structure
        self.number_of_variants = number_of_variants


        self.task_parameters = {'Spline': {'x1': -5,
                                           'x2': 5,
                                           'y1': -20,
                                           'y2': 20,
                                           'step': 1},
                                'Trapezoid': {'n': 11},
                                'Simpson': {'n': 9},
                                'Interpolation': {'degree': 3}
                                }

    def set_task_parameters(self, task_name, parameters_to_set):
        parameters = self.task_parameters[task_name]
        if parameters:
            for key in parameters:
                parameter = parameters_to_set[key]
                if parameter is not None:
                    parameters[key] = parameter

    def generate_tasks(self):
        variants_list = []
        for variant_n in range(1, self.number_of_variants + 1):
            tasks_list = []
            for task_name in self.structure:
                parameters = self.task_parameters[task_name]
                if parameters is not None:
                    if task_name == 'Spline':
                        task = SplineTask.randomize(x_range=(parameters['x1'], parameters['x2']),
                                                    y_range=(parameters['y1'], parameters['y2']),
                                                    step=parameters['step'])
                    if task_name == 'Trapezoid':
                        task = TrapezoidTask().randomize(parameters['n'])
                    if task_name == 'Simpson':
                        task = SimpsonTask().randomize(parameters['n'])
                    if task_name == 'Interpolation':
                        task = InterpolationTask(degree=(parameters['degree']))
                    tasks_list.append(task)
            variants_list.append(tasks_list)

        return variants_list
