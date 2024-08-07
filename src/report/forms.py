from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput

from .models import ReportModel, ImageUpload


class ReportModelForm(forms.ModelForm):
    date = forms.DateField(
        label='作成日',
        widget=DatePickerInput(format='%Y-%m-%d')
    )
    class Meta:
        model = ReportModel
        exclude = ['user', 'slug']

    def __init__(self, user=None, *args, **kwargs):
        #デフォルト値
        self.user = user
        self.base_fields['title'].initial = 'default'
        #クラス付与
        for key, field in self.base_fields.items():
            if key != "public":
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-check-input"
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        report_obj = super().save(commit=False)
        if self.user:
            report_obj.user = self.user
        if commit:
            report_obj.save()
        return report_obj


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = '__all__'