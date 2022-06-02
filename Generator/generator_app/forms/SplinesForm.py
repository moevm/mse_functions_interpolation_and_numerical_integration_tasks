import re
from django import forms
from .InterpolationForm import variants_type_choices, generation_format_choices


class SplinesForm(forms.Form):
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

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('generation_format') is None:
            raise forms.ValidationError("Выберите формат генерации")
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

