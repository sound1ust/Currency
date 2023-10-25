from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from converter.models import Source, Converter


class DatesForm(forms.Form):
    start_date = forms.DateField(widget=AdminDateWidget)
    end_date = forms.DateField(widget=AdminDateWidget)


class SourceAdminForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get('autoload_method').startswith('get_'):
            self.add_error(
                'autoload_method',
                "Autoload method must starts with 'get_'"
            )

        return cleaned_data


class ConverterForm(forms.ModelForm):
    class Meta:
        model = Converter
        fields = '__all__'
