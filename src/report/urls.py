from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report-list'),
    path('detail/<slug:slug>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('create/', views.ReportCreateFormView.as_view(), name='report-create'),
    path('update/<slug:slug>/', views.ReportUpdateFormView.as_view(), name='report-update'),
    path('delete/<slug:slug>/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('image-upload/', views.ImageUploadView.as_view(), name='image-upload'),
]