from django.db import models
from django.contrib.auth import get_user, get_user_model


User = get_user_model()

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


class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to=save_path)

    def __str__(self):
        return self.title