from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

from accounts.models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_email = self.instance.user.email
        if username == user_email:
            raise ValidationError(_('ユーザー名を変更してください'), code='invalid username')
        elif '@' in username:
            raise ValidationError(_('ユーザー名にEメールアドレスは使用できません'), code='no email')
        return username