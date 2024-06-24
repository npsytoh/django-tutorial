from django import forms
from .models import ImageUpload

class ReportFormClass(forms.Form):

    def __init__(self, *args, **kwargs):

        #デフォルト値
        self.base_fields['title'].initial = 'default'

        #クラス付与
        for field in self.base_fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        super().__init__(*args, **kwargs)

    title = forms.CharField(label='タイトル', widget=forms.TextInput(attrs={'placeholder':'タイトル'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'内容...'}), label='内容')

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = '__all__'