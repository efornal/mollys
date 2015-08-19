# -*- encoding: utf-8 -*-
from django.test import TestCase

from .models import Person

class PersonTests(TestCase):

    
    def test_compose_suggested_name(self):
        name = 'Alan Mathison'
        surname = 'Turing'
        self.assertEqual( Person.compose_suggested_name(surname, name), 'aturing')

    def test_compose_suggested_name_between_spaces(self):
        name = ' Alan Mathison '
        surname = 'Turing'
        self.assertEqual( Person.compose_suggested_name(surname, name), 'aturing')

    def test_compose_suggested_name_with_compose_surname(self):
        name = 'Alan Mathison'
        surname = 'Turing Wilmslow'
        self.assertEqual( Person.compose_suggested_name(surname, name), 'aturing')

    def test_compose_suggested_name_with_compose_surname_and_spaces(self):
        name = ' Alan  Mathison '
        surname = ' Turing  Wilmslow '
        self.assertEqual( Person.compose_suggested_name(surname, name), 'aturing')

    def test_compose_suggested_name_with_simple_name_and_surname(self):
        name = 'Alan'
        surname = 'Turing'
        self.assertEqual( Person.compose_suggested_name(surname, name), 'aturing')

        
    def test_compose_extended_suggested_name(self):
        name = 'Alan Mathison'
        surname = 'Turing'
        self.assertEqual( Person.compose_extended_suggested_name(surname, name), 'amturing')

    def test_compose_extended_suggested_name_with_compose_surname(self):
        name = 'Alan Mathison'
        surname = 'Turing Wilmslow'
        self.assertEqual( Person.compose_extended_suggested_name(surname, name), 'amturing')

    def test_compose_extended_suggested_name_with_compose_surname_and_spaces(self):
        name = ' Alan  Mathison '
        surname = ' Turing  Wilmslow '
        self.assertEqual( Person.compose_extended_suggested_name(surname, name), 'amturing')

    def test_compose_extended_suggested_name_with_simple_name_and_surname(self):
        name = 'Alan'
        surname = 'Turing'
        self.assertEqual( Person.compose_extended_suggested_name(surname, name), 'aturing')

    def test_compose_extended_suggested_name_with_simple_name_and_surname(self):
        name = 'Alan'
        surname = 'Turing'
        self.assertEqual( Person.compose_extended_suggested_name(surname, name), 'aturing')


    def test_strip_accents_without_accents(self):
        self.assertEqual(Person.strip_accents('Veronica Ojeda'), 'Veronica Ojeda')

    def test_strip_accents_with_accents(self):
        self.assertEqual(Person.strip_accents('Verónica Ojeda'), 'Veronica Ojeda')

    def test_strip_accents_with_accents_and_spaces(self):
        self.assertEqual(Person.strip_accents('Verónica  Ojeda '), 'Veronica  Ojeda ')

