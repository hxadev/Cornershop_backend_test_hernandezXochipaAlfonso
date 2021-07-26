import datetime

from Modules.MenuOrdersApp.models import *
from django.test import TestCase
from django.utils import timezone


class TestModelsCase(TestCase):
    @classmethod
    def create_menu(cls):
        return Menus.objects.create(publisheddate=timezone.now(
            ), createdat=timezone.now())

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_create_menu(self):
        menu=self.create_menu()
        self.assertTrue(isinstance(menu,Menus))
