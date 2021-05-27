from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class tViewTest(TestCase):
    # URL Exists
    def test_view_url_exists_at_desired_location_predict(self):
        response = self.client.get('/predict')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_exists_at_desired_location_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_desired_location_classify(self):
            response = self.client.get('/classify')
            self.assertEqual(response.status_code, 200)

    # By Name
    def test_view_url_accessible_by_name_predict(self):
        response = self.client.get(reverse('predict'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name_classify(self):
        response = self.client.get(reverse('classify'))
        self.assertEqual(response.status_code, 200)

    # Correct Templates
    def test_view_uses_correct_template_predict(self):
        response = self.client.get(reverse('predict'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'predict.html')
    
    def test_view_uses_correct_template_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_view_uses_correct_template_(self):
        response = self.client.get(reverse('classify'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classify.html')