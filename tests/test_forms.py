# -*- encoding: utf-8 -*-
from django.test import TestCase
from app.forms import PersonForm

class PersonFormTests(TestCase):

    def test_capitalized_name(self):
        form_data = {'name': 'juan albERTO', 'surname': 'perez'}
        form = PersonForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['name'], 'Juan Alberto')

    def test_capitalized_surname(self):
        form_data = {'name': 'juan', 'surname': 'perez siMONello'}
        form = PersonForm(data=form_data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['surname'], 'Perez Simonello')
