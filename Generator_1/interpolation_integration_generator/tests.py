import django.test
from interpolation_integration_generator.forms.IntegrationForm import IntegrationForm
from interpolation_integration_generator.forms.InterpolationForm import InterpolationForm


class Test(django.test.SimpleTestCase):
    def test_homePage(self):
        page = self.client.get('/')
        self.assertEqual(page.status_code, 200)

    def test_integrationPage(self):
        page = self.client.get('/integration/')
        self.assertEqual(page.status_code, 200)

    def test_interpolationPage(self):
        page = self.client.get('/interpolation/')
        self.assertEqual(page.status_code, 200)

    def test_integrationForm(self):
        form1 = IntegrationForm({'variants_type': 'digits', 'generation_format': 'tex'})
        form2 = IntegrationForm({})
        form3 = IntegrationForm({'filename': '8304_2sem', 'number_of_variants': 30, 'variants_type': 'digits',
                                 'file_with_surnames': None, 'generation_format': ['pdf'], 'seed': None,
                                 'number_of_trapezoid_points': 10, 'number_of_Simpson_points': 10})

        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertTrue(form3.is_valid())

    def test_interpolationForm(self):
        form1 = InterpolationForm({'number_of_variants': 30, 'number_of_variants_in_string': 2})
        form2 = InterpolationForm({})
        form3 = InterpolationForm({'filename': '8304_2sem', 'number_of_variants': 30, 'number_of_variants_in_string': 2,
                                 'the_biggest_polynomial_degree': 3, 'variants_type': 'digits',
                                 'file_with_surnames': None, 'generation_format': ['pdf'], 'seed': None})

        self.assertFalse(form1.is_valid())
        self.assertFalse(form2.is_valid())
        self.assertTrue(form3.is_valid())

    def test_incorrectUrls(self):
        page1 = self.client.get('/generate_integration/')
        page2 = self.client.get('/generate_interpolation/')

        self.assertNotEqual(page1.status_code, 200)
        self.assertNotEqual(page2.status_code, 200)


