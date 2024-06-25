from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy
from .models import ReportModel
from .forms import ReportModelForm
from .forms import ImageUploadForm


class ReportListView(ListView):
    template_name = 'report/report-list.html'
    context_object_name = 'object_lists'
    model = ReportModel

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['page_title'] = '一覧'
        return ctx


class ReportDetailView(DetailView):
    template_name = 'report/report-detail.html'
    context_object_name = 'objects'
    model = ReportModel


class ReportCreateFormView(FormView):
    template_name = 'report/report-form.html'
    form_class = ReportModelForm
    success_url = reverse_lazy('report:report-list')

    def form_valid(self, form):
        data = form.cleaned_data
        obj = ReportModel(**data)
        obj.save()
        return super().form_valid(form)


class ReportUpdateFormView(UpdateView):
    template_name = 'report/report-form.html'
    model = ReportModel
    form_class = ReportModelForm
    success_url = reverse_lazy('report:report-list')


class ReportDeleteView(DeleteView):
    template_name = 'report/report-delete.html'
    context_object_name = 'objects'
    model = ReportModel
    success_url = reverse_lazy('report:report-list')


class ImageUploadView(CreateView):
    template_name = 'report/image-upload.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('report:report-list')