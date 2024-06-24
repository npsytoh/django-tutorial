from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from .models import ReportModel
from .forms import ReportFormClass
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


def reportCreateView(request):
    template_name = 'report/report-form.html'
    form = ReportFormClass(request.POST or None)
    ctx = {
        'form': form
    }

    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        obj = ReportModel(title=title, content=content)
        obj.save()
        return redirect('report:report-list')

    return render(request, template_name, ctx)


def reportUpdateView(request, pk):
    template_name = 'report/report-form.html'
    #obj = ReportModel.objects.get(pk=pk)
    obj = get_object_or_404(ReportModel, pk=pk)
    initial_values = {'title': obj.title, 'content': obj.content}
    form = ReportFormClass(request.POST or initial_values)
    ctx = {
        'form': form
    }

    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        obj.title = title
        obj.content = content
        obj.save()

        if request.method == 'POST':
            return redirect('report:report-list')

    return render(request, template_name, ctx)


def reportDeleteView(request, pk):
    template_name = 'report/report-delete.html'
    obj = get_object_or_404(ReportModel, pk=pk)
    ctx = {'objects': obj}
    if request.method == 'POST':
        obj.delete()
        return redirect('report:report-list')
    return render(request, template_name, ctx)

class ImageUploadView(CreateView):
    template_name = 'report/image-upload.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('report:report-list')