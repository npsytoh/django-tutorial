from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class OwnerOnly(UserPassesTestMixin):
    def test_func(self):
        report_instance = self.get_object()
        return report_instance.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'ご自身の日報でのみ編集・削除可能です')
        return redirect('report:report-detail', pk=self.kwargs['pk'])

class OwnProfileOnly(UserPassesTestMixin):
    def test_func(self):
        profile_obj = self.get_object()
        try:
            return profile_obj == self.request.user.profile
        except:
            return False