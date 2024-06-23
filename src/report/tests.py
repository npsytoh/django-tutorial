from django.test import TestCase
from django.urls import reverse
from .models import ReportModel


class ReportTestCase(TestCase):
    
    #初期設定
    def setUp(self):
        obj = ReportModel(title='testTitle1', content='testContent1')
        obj.save()
    
    #DB保存の検証
    def test_saved_single_object(self):
        qs_count = ReportModel.objects.count()
        self.assertEqual(qs_count, 1)
    
    #存在しないレコードに404を返すか検証
    def test_response_404(self):
        detail_url = reverse('report:report-detail', kwargs={"pk": 100})
        detail_response = self.client.get(detail_url)
        update_url = reverse('report:report-update', kwargs={"pk": 100})
        update_response = self.client.get(update_url)
        delete_url = reverse('report:report-delete', kwargs={"pk": 100})
        delete_response = self.client.get(delete_url)
        self.assertEqual(detail_response.status_code, 404)
        self.assertEqual(update_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
    
    #CREATEの検証
    def test_create_on_createView(self):
        url = reverse('report:report-create')
        create_data = {"title": "title_from_test", "content": "content_from_test"}
        response = self.client.post(url, create_data)
        qs_counter2 = ReportModel.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(qs_counter2, 2)