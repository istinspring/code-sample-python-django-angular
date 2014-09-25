from datetime import date

from django.test import TestCase

from django.db import models


class ModelsTestCase(TestCase):
    def setUp(self):
        self.model_class = models.get_model('main', 'Items')
        self.model_class.objects.create(
            title="item one", rating=11, date=date(year=2008, month=11, day=13))
        self.model_class.objects.create(
            title="item two", rating=16, date=date(year=2008, month=11, day=13))

    def test_animals_can_speak(self):
        one = self.model_class.objects.get(rating=11)
        two = self.model_class.objects.get(title="item two")

        self.assertEqual(one.title, "item one")
        self.assertEqual(two.rating, 16)
