from django.contrib import admin
from . import models

admin.site.register(models.ReportModel)
admin.site.register(models.ImageUpload)