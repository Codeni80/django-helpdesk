from django.test import TestCase
from ticketing.models import *

class ModelTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false")
        self.assertFalse(False)

    def test_true_is_true(self):
        print("Method: test_true_is_true")
        self.assertTrue(True)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two")
        self.assertEqual(1 + 1, 2)

    def test_object_name_is_first_space_last(self):
        user = CustomUser.objects.get(pk=1)
        expected_object_name = f'{user.u_name}'
        self.assertEquals(expected_object_name, str(author))
