from django.db import models


def save_path(instance, filename):
    ext = filename.split('.')[-1]
    new_name = instance.title + '_saved'
    return f'files/{new_name}.{ext}'

class ReportModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(upload_to=save_path)

    def __str__(self):
        return self.title