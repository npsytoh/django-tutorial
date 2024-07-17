from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from utils.access_restrictions import OwnProfileOnly
from .models import Profile
from .forms import ProfileUpdateForm


class ProfileUpdateView(OwnProfileOnly, UpdateView):
    template_name = "account/profile-form.html"
    model = Profile
    form_class=ProfileUpdateForm
    success_url = reverse_lazy("report:report-list")