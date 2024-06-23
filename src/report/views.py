from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import ReportModel
from .forms import ReportFormClass
from .forms import ImageUploadForm


def reportListView(request):
    template_name = 'report/report-list.html'
    obj = ReportModel.objects.all()
    ctx = {
        'object_lists': obj
    }
    return render(request, template_name, ctx)


def reportDetailView(request, pk):
    template_name = 'report/report-detail.html'
    #obj = ReportModel.objects.get(pk=pk)
    obj = get_object_or_404(ReportModel, pk=pk)
    ctx = {
        'objects': obj,
    }
    return render(request, template_name, ctx)


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