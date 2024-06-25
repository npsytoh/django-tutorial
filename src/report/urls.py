from django.urls import path
from . import views

app_name = 'report'

urlpatterns = [
    path('', views.ReportListView.as_view(), name='report-list'),
    path('detail/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('create/', views.ReportCreateFormView.as_view(), name='report-create'),
    path('update/<int:pk>/', views.ReportUpdateFormView.as_view(), name='report-update'),
    path('delete/<int:pk>/', views.ReportDeleteView.as_view(), name='report-delete'),
    path('image-upload/', views.ImageUploadView.as_view(), name='image-upload'),
]