from django import forms

from .InterpolationForm import variants_type_choices, generation_format_choices


class IntegrationForm(forms.Form):
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

    seed = forms.IntegerField(
        label='Сид для генерации:',
        required=False,
    )

    number_of_trapezoid_points = forms.IntegerField(
        label='Количество точек: (формула Трапеции)',
        min_value=1,
        max_value=15,
        initial=10,
    )

    number_of_Simpson_points = forms.IntegerField(
        label='Количество точек: (формула Симпсона)',
        min_value=1,
        max_value=15,
        initial=10,
    )

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data.get('generation_format')) == 0:
            raise forms.ValidationError("You need to choice at least one generation format.")

        variants_types = ['digits', 'surnames']
        if cleaned_data.get('variants_type') not in variants_types:
            raise forms.ValidationError("Variants types must be digits ot surnames.")
