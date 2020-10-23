from Tasks import Tasks

degree = int(input("Степень многочлена: "))
options_summary = int(input("Количество вариантов: "))
options_in_line = int(input("Количество вариантов в строке (2, 3): "))

document = Tasks(options_summary, options_in_line, degree)
document.generate()
