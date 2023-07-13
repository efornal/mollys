# -*- encoding: utf-8 -*-
from django.test import TestCase

from app.models import Person

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



    def test_ldap_user_valid(self):
        self.assertTrue( Person.ldap_user_name_valid('petros') )

    def test_ldap_user_with_space(self):
        self.assertFalse( Person.ldap_user_name_valid(' petros ') )

    def test_ldap_user_with_middle_space(self):
        self.assertFalse( Person.ldap_user_name_valid('petros jose') )

    def test_ldap_user_with_backslash(self):
        self.assertFalse( Person.ldap_user_name_valid('petros/lei') )

    def test_ldap_user_with_point(self):
        self.assertFalse( Person.ldap_user_name_valid('petros.') )

    def test_ldap_user_with_acent(self):
        self.assertFalse( Person.ldap_user_name_valid('petrós') )

    def test_ldap_user_with_number(self):
        self.assertTrue( Person.ldap_user_name_valid('petr5s') )


    def test_ldap_password_valid(self):
        self.assertTrue( Person.ldap_password_valid('elprofes') )

    def test_ldap_password_valid_with_special_characters(self):
        self.assertTrue( Person.ldap_password_valid('elprofes @#$%^&+=') )

    def test_ldap_password_numeric_valid(self):
        self.assertTrue( Person.ldap_password_valid('12345678') )

    def test_ldap_password_too_short(self):
        self.assertFalse( Person.ldap_password_valid('elprof') )

    def test_ldap_password_hash_valid(self):
        self.assertTrue( Person.ldap_password_valid('{SSHA}DJtONDDSJ3SnEKRJ0aMDzUMOkMOsOhp/') )
