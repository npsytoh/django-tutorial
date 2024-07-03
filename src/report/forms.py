from django import forms
from .models import ReportModel, ImageUpload

class ReportModelForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        exclude = ['user']

    def __init__(self, user=None, *args, **kwargs):
        #デフォルト値
        self.user = user
        self.base_fields['title'].initial = 'default'
        #クラス付与
        for field in self.base_fields.values():
            field.widget.attrs.update({'class': 'form-control'})
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