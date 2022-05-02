from django import forms
from django.core.files.uploadedfile import UploadedFile

task_choices = (
    ('Interpolation_Lagrange', 'Интерполяционный многочлен по формуле Лагранжа'),
    ('Interpolation_Forward', 'Интерполяционный многочлен по формуле Ньютона (интерполяция вперед)'),
    ('Interpolation_Back', 'Интерполяционный многочлен по формуле Ньютона (интерполяция назад)'),
)

number_of_variants_in_string_choices = (
    (2, 2),
    (3, 3),
)

the_biggest_polynomial_degree_choices = (
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
)

variants_type_choices = (
    ('digits', 'Числами'),
    ('surnames', 'Пофамильно')
)

generation_format_choices = (
    ('pdf', 'pdf'),
    ('tex', 'tex'),
)

alternate_choices = (
    ('not_alternate', 'Без чередования'),
    ('alternate', 'Чередовать задания')
)


class InterpolationForm(forms.Form):
    file: UploadedFile = None
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

    # TODO: remove or add support
    '''
    number_of_variants_in_string = forms.IntegerField(
        label='Количество вариантов в строке:',
        initial=2,
        widget=forms.RadioSelect(
            choices=number_of_variants_in_string_choices,
        ),
    )
    '''

    the_biggest_polynomial_degree = forms.IntegerField(
        label='Наибольшая степень многочлена:',
        initial=3,
        widget=forms.RadioSelect(
            choices=the_biggest_polynomial_degree_choices,
        ),
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

    tasks = forms.MultipleChoiceField(
        label='Задания:',
        choices=task_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    alternate = forms.ChoiceField(
        label='Чередование:',
        initial='not_alternate',
        choices=alternate_choices,
        widget=forms.RadioSelect(),
    )

    generation_format = forms.MultipleChoiceField(
        label='Формат генерации:',
        initial='pdf',
        choices=generation_format_choices,
        widget=forms.CheckboxSelectMultiple(),
    )

    seed = forms.IntegerField(
        label='Сид для генерации:',
        required=False,
    )

    def set_file(self, file: UploadedFile):
        InterpolationForm.file = file

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('generation_format') is None:
            raise forms.ValidationError("Выберите формат генерации")

        variants_types = ['digits', 'surnames']
        variants_type = cleaned_data.get('variants_type')
        if variants_type not in variants_types:
            raise forms.ValidationError("Variants types must be digits ot surnames.")
        if variants_type == 'digits' and cleaned_data.get('number_of_variants') is None:
            raise forms.ValidationError("Укажите количество вариантов")
