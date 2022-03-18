from django import forms

from .InterpolationForm import variants_type_choices, generation_format_choices


class SplinesForm(forms.Form):
    def clean(self):
        pass
