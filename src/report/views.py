from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q

from utils.access_restrictions import OwnerOnly
from accounts.models import Profile
from .models import ReportModel
from .forms import ReportModelForm
from .forms import ImageUploadForm
from .filters import ReportModelFilter


class ReportListView(ListView):
    template_name = 'report/report-list.html'
    context_object_name = 'object_lists'
    model = ReportModel

    def get_queryset(self):
        qs = ReportModel.objects.all()
        if self.request.user.is_authenticated:
            qs = qs.filter(Q(public=True)|Q(user=self.request.user))
        else:
            qs = qs.filter(public=True)
        qs = qs.order_by('-date')
        return qs

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx['page_title'] = '一覧'
        ctx['filter'] = ReportModelFilter(self.request.GET, queryset=self.get_queryset())
        profile_id = self.request.GET.get('profile')
        q = Profile.objects.filter(id=profile_id)
        if q.exists():
            ctx['profile'] = q.first()
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