import re
from django import forms
from .InterpolationForm import variants_type_choices, generation_format_choices, the_biggest_polynomial_degree_choices

task_choices = (
    ('Interpolation_Lagrange', 'Интерполяционный многочлен по формуле Лагранжа'),
    ('Interpolation_Forward', 'Интерполяционный многочлен по формуле Ньютона (интерполяция вперед)'),
    ('Interpolation_Back', 'Интерполяционный многочлен по формуле Ньютона (интерполяция назад)'),
    ('Trapezoid', 'Интегрирование по формуле трапеций'),
    ('Simpson', 'Интегрирование по формуле Симпсона'),
    ('Spline', 'Вычисление коэффициентов параболического сплайна')
)

alternate_choices = (
    ('alternate_interpolation', 'Чередовать задания по интерполированию'),
    ('alternate_integration', 'Чередовать задания по интегрированию')
)


class CustomVariantsForm(forms.Form):
    filename = forms.CharField(
        label='Имя файла:',
        max_length=30,
        initial='8304_2sem',
    )

    number_of_variants = forms.IntegerField(
        label='Количество вариантов:',
        min_value=1,
        max_value=100,
        initial=30,
        required=False,
    )

    variants_type = forms.ChoiceField(
        label='Нумерация вариантов:',
        initial='digits',
        choices=variants_type_choices,
        widget=forms.RadioSelect,
    )

    file_with_surnames = forms.FileField(
        required=False,
    )

    generation_format = forms.MultipleChoiceField(
        label='Формат генерации:',
        initial='pdf',
        choices=generation_format_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    tasks = forms.MultipleChoiceField(
        label='Задания:',
        choices=task_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    the_biggest_polynomial_degree = forms.IntegerField(
        label='Наибольшая степень многочлена:',
        initial=3,
        widget=forms.RadioSelect(
            choices=the_biggest_polynomial_degree_choices,
        ),
    )

    number_of_trapezoid_points = forms.IntegerField(
        label='Количество точек: (формула Трапеции)',
        min_value=3,
        max_value=15,
        initial=11,
    )

    number_of_Simpson_points = forms.IntegerField(
        label='Количество точек: (формула Симпсона)',
        min_value=3,
        max_value=15,
        initial=9,
    )

    Splines_x1 = forms.IntegerField(
        label='Нижняя граница x:',
        initial=-5,
        required=False,
    )

    Splines_x2 = forms.IntegerField(
        label='Верхняя граница x:',
        initial=5,
        required=False,
    )

    Splines_y1 = forms.FloatField(
        label='Нижняя граница y:',
        initial=-20,
        required=False,
    )

    Splines_y2 = forms.FloatField(
        label='Верхняя граница y:',
        initial=20,
        required=False,
    )

    Splines_step = forms.IntegerField(
        label='Шаг:',
        initial=1,
        required=False,
        min_value=1,
    )

    seed = forms.IntegerField(
        label='Сид для генерации:',
        required=False,
    )

    alternate = forms.MultipleChoiceField(
        label='Чередование заданий:',
        required=False,
        choices=alternate_choices,
        widget=forms.CheckboxSelectMultiple()
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('generation_format') is None:
            raise forms.ValidationError("Выберите формат генерации")
        if cleaned_data.get('tasks') is None:
            raise forms.ValidationError("Выберите хотя бы одно задание")
        if not re.match(r'^\w+$', cleaned_data.get('filename')) and len(cleaned_data.get('filename')) <= 255:
            print(cleaned_data.get('filename'))
            raise forms.ValidationError("Введите имя файла, состоящее из букв, цифр и нижнего подчёркивания")

        if cleaned_data.get('Splines_x1') > cleaned_data.get('Splines_x2'):
            raise forms.ValidationError("Верхняя граница по x меньше нижней границы")
        if cleaned_data.get('Splines_y1') > cleaned_data.get('Splines_y2'):
            raise forms.ValidationError("Верхняя граница по y меньше нижней границы")
        if cleaned_data.get('Splines_step') > abs(cleaned_data.get('Splines_x1') - cleaned_data.get('Splines_x2')):
            raise forms.ValidationError("Шаг превышает размер отрезка между нижней и верхней границами")
        variants_types = ['digits', 'surnames']
        variants_type = cleaned_data.get('variants_type')
        if variants_type not in variants_types:
            raise forms.ValidationError("Variants types must be digits or surnames.")
        if variants_type == 'digits' and cleaned_data.get('number_of_variants') is None:
            raise forms.ValidationError("Укажите количество вариантов")
