from Tasks import Tasks
from timeit import Timer

generate_by_name = False

# n = int(input("Степень многочлена: "))
# options_summary = int(input("Количество вариантов: "))
# options_in_line = int(input("Количество вариантов в строке (2, 3): "))
degree = 4
options_summary = 13
options_in_line = 3

document = Tasks(options_summary, options_in_line, degree)
document.generate()
