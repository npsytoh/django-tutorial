from django.test import TestCase
from report.models import ReportModel
from django.urls import reverse

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

class ReportTestCase(TestCase):
    def __init__(self, *args, **kwargs):
        self.email = "test@sample.jp"
        self.password = "testpassword"
        self.title = "testTitle1"
        self.content = "testContent1"
        self.slug = "some-slug-for-test"
        super().__init__(*args, **kwargs)

    #初期設定
    def setUp(self):
        user_obj = User(email=self.email)
        user_obj.set_password(self.password)
        user_obj.save()
        email_obj = EmailAddress(user=user_obj, email=self.email, verified=True)
        email_obj.save()
        self.user_obj = user_obj
        report_obj = ReportModel(user=user_obj, title=self.title, content=self.content)
        report_obj.save()

    #日報の作成ができているか
    def test_saved_single_object(self):
        qs_counter = ReportModel.objects.count()
        self.assertEqual(qs_counter, 1)

    #ユーザーが作られているか
    def test_user_saved(self):
        counter = User.objects.count()
        self.assertEqual(counter, 1)
        email_counter = EmailAddress.objects.count()
        self.assertEqual(email_counter, 1)

    #メールがverifiedになっているか
    def test_email_verified(self):
        email_obj = EmailAddress.objects.first()
        self.assertEqual(True, email_obj.verified)

    #ログインページが機能しているか
    def test_login(self):
        data = {"email": self.email, "password": self.password}
        response = self.client.post("/accounts/login/", data)
        self.assertEqual(response.status_code, 200)

    #新規登録ページが機能しているか
    def test_signup(self):
        new_data = {"email": "test2@sample.jp", "password1": "testpassword2", "password2": "testpassword2"}
        redirect_to = reverse("account_email_verification_sent")
        response = self.client.post("/accounts/signup/", new_data)
        #Email Confirmationへredirectされているか？
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, redirect_to)
        #ユーザーが作られているか？
        self.assertEqual(User.objects.count(), 2)

    #queryが存在しない時に、404ページを返すかどうか
    def test_response_404(self):
        detail_url = reverse('report:report-detail', kwargs={"slug": "slug-not-exist"})
        detail_response = self.client.get(detail_url)
        update_url = reverse('report:report-update', kwargs={"slug": "slug-not-exist"})
        update_response = self.client.get(update_url)
        delete_url = reverse('report:report-delete', kwargs={"slug": "slug-not-exist"})
        delete_response = self.client.get(delete_url)
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
#Anonymousユーザーはアクセスできない
    def test_access_to_createview(self):
        url = reverse("report:report-create")
        redirect_to = reverse("account_login")
        response = self.client.get(url)
        self.assertRedirects(response, f"{redirect_to}?next=/report/create/")

#ログインユーザーが日報を作成する
    def test_create_on_createView(self):
        user_obj = User.objects.first()
        url = reverse('report:report-create')
        create_data = {"user": user_obj, "title": "title_from_test", "content": "content_from_test", "slug":"some-random-slug"}
        self.client.login(email=self.email, password=self.password)
        response = self.client.post(url, create_data)
        redirect_to = reverse("report:report-list")
        qs_counter2 = ReportModel.objects.count()
        self.assertRedirects(response, redirect_to)
        self.assertEqual(qs_counter2, 2)

#別のユーザーではアップデートできない
    def test_update_with_another_user(self):
        another_user = User(email="test2@sample.jp")
        another_user.set_password("testpassword2")
        another_user.save()
        self.client.login(email=another_user.email, password=another_user.password)
        report_obj = ReportModel.objects.first()
        redirect_to = reverse("report:report-detail", kwargs={"slug":report_obj.slug})
        url = reverse('report:report-update', kwargs={"slug": report_obj.slug})
        response = self.client.get(url)
        self.assertRedirects(response, redirect_to)

#自分の日報はアップデートできる
    def test_update_with_own_user(self):
        self.client.login(email=self.email, password=self.password)
        report_obj = ReportModel.objects.first()
        url = reverse('report:report-update', kwargs={"slug": report_obj.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_with_another_user(self):
        another_user = User(email="test2@sample.jp")
        another_user.set_password("testpassword2")
        another_user.save()
        self.client.login(email=another_user.email, password=another_user.password)
        report_obj = ReportModel.objects.first()
        redirect_to = reverse("report:report-detail", kwargs={"slug":report_obj.slug})
        url = reverse('report:report-delete', kwargs={"slug": report_obj.slug})
        response = self.client.post(url, {})
        self.assertRedirects(response, redirect_to)

    def test_delete_with_own_user(self):
        redirect_to = reverse("report:report-list")
        self.client.login(email=self.email, password=self.password)
        report_obj = ReportModel.objects.first()
        url = reverse('report:report-delete', kwargs={"slug": report_obj.slug})
        response = self.client.post(url, {})
        self.assertRedirects(response, redirect_to)

    def test_listview_with_anonymous(self):
        self.client.logout()#logoutの実行
        url = reverse("report:report-list")
        response = self.client.get(url)
        object_list = response.context_data["object_list"]
        self.assertEqual(len(object_list), 0)

    def test_listview_with_own_user(self):
        url = reverse("report:report-list")
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(url)
        object_list = response.context_data["object_list"]
        self.assertEqual(len(object_list), 1)

#日報を作成する（テストではない）
    def make_report(self, user, public):
        report_obj = ReportModel(user=user, public=public)
        report_obj.title = f"title {report_obj.pk}"
        report_obj.content = f"content {report_obj.pk}"
        report_obj.save()
        return report_obj

    #サーチフォームテスト
    def test_search_queryset(self):
        user_obj = User.objects.get(email=self.email)
        test_user = User(email="test2@sample.jp")
        test_user.set_password("testpassword2")
        test_user.save()
        obj1 = self.make_report(user=user_obj, public=True)
        obj2 = self.make_report(user=user_obj, public=False)
        obj3 = self.make_report(user=test_user, public=True)
        obj4 = self.make_report(user=test_user, public=False)
        counter = ReportModel.objects.count()
        self.assertEqual(counter, 5)
        self.client.login(email=self.email, password=self.password)
        response = self.client.get(reverse("report:report-list"))
        self.assertEqual(len(response.context_data["object_list"]), 4)
        url = reverse("report:report-list") + "?search=1"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data["object_list"]), 1)
        url = reverse("report:report-list") + "?search=content"
        response = self.client.get(url)
        self.assertEqual(len(response.context_data["object_list"]), 4)

    #SlugFieldにデフォルト値が格納されているか
    def test_slug_saved(self):
        report_obj = ReportModel.objects.first()
        self.assertTrue(report_obj.slug)