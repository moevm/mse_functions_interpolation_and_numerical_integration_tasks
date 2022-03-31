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

    x1 = forms.IntegerField(
        label='Нижняя граница x:',
        initial=-5,
        required=False,
    )

    x2 = forms.IntegerField(
        label='Верхняя граница x:',
        initial=5,
        required=False,
    )

    y1 = forms.FloatField(
        label='Нижняя граница y:',
        initial=-20,
        required=False,
    )

    y2 = forms.FloatField(
        label='Верхняя граница y:',
        initial=20,
        required=False,
    )

    step = forms.IntegerField(
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
        pass
