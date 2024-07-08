from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import ReportModel
from .forms import ReportModelForm
from .forms import ImageUploadForm


class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        report_instance = self.get_object()
        return report_instance.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'ご自身の日報でのみ編集・削除可能です')
        return redirect('report:report-detail', pk=self.kwargs['pk'])


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


class ReportCreateFormView(LoginRequiredMixin, FormView):
    template_name = 'report/report-form.html'
    form_class = ReportModelForm
    success_url = reverse_lazy('report:report-list')

    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs['user'] = self.request.user
        return kwgs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class ReportUpdateFormView(OwnerOnly, UpdateView):
    template_name = 'report/report-form.html'
    model = ReportModel
    form_class = ReportModelForm
    success_url = reverse_lazy('report:report-list')


class ReportDeleteView(OwnerOnly, DeleteView):
    template_name = 'report/report-delete.html'
    context_object_name = 'objects'
    model = ReportModel
    success_url = reverse_lazy('report:report-list')


class ImageUploadView(CreateView):
    template_name = 'report/image-upload.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('report:report-list')