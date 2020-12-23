import django.test


class Test(django.test.TestCase):
    def test_a(self):
       self.assertEqual(1, 1)