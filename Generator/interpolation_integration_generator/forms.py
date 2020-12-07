from django import forms


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


class InterpolationForm(forms.Form):
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

    number_of_variants_in_string = forms.IntegerField(
        label='Количество вариантов в строке:',
        initial=2,
        widget=forms.RadioSelect(
            choices=number_of_variants_in_string_choices,
        ),
    )

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
        required = True,
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

    seed = forms.IntegerField(
        label='Сид для генерации:',
        required=False,
    )

