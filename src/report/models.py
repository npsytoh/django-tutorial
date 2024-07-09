from django.db import models
from django.contrib.auth import get_user, get_user_model


User = get_user_model()

GENDER_CHOICE = [(None, "--"), ("m", "男性"), ("f", "女性")]

def save_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = instance.title + '_saved'
    return f'files/{new_name}.{ext}'


class ReportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.TextField(max_length=1000, verbose_name='内容')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta():
        verbose_name = '日報'
        verbose_name_plural = '日報一覧'

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, verbose_name="ユーザー名")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部署")
    phone_number = models.IntegerField(blank=True, null=True, verbose_name="携帯番号")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, default=None, verbose_name="性別", blank=True, null=True)
    birthday = models.DateField(blank=True, null=True, verbose_name="生年月日")

    def __str__(self):
        return self.username


class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to=save_path)

    def __str__(self):
        return self.title