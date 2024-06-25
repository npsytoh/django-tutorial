from django import forms
from .models import ReportModel, ImageUpload

class ReportModelForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        #デフォルト値
        self.base_fields['title'].initial = 'default'
        #クラス付与
        for field in self.base_fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        super().__init__(*args, **kwargs)


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = '__all__'