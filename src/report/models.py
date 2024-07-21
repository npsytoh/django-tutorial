from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils import timezone

from utils.random_string import random_string_generator


User = get_user_model()

def slug_maker():
    repeat = True
    while repeat:
        new_slug = random_string_generator()
        counter = ReportModel.objects.filter(slug=new_slug).count()
        if counter == 0:
            repeat = False
    return new_slug

def get_profile_page_url(self):
    from django.urls import reverse_lazy
    return reverse_lazy('report:report-list') + f'?profile={self.user.profile.id}'

def save_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = instance.title + '_saved'
    return f'files/{new_name}.{ext}'

class ReportModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100, verbose_name='タイトル')
    content = models.TextField(max_length=1000, verbose_name='内容')
    timestamp = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False, verbose_name='公開する')
    slug = models.SlugField(max_length=20, unique=True, default=slug_maker)

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