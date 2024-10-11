import unittest

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
# from borrowers.models import Borrowers
from renters.models import Renters


class RentersModelTest(TestCase):
    def setUp(self):
        # Create an initial borrower with a specific email
        self.renter = Renters.objects.create(
            first_name='Moses',
            last_name='Ochieng',
            email='mosesa.ochieng@gmail.com',
            phone_number='0701234568',
            password='',
            username='Moses.Ochieng',
        )

    def test_renter_creation(self):
        self.assertEqual(self.renter.first_name, 'Moses')
        self.assertEqual(self.renter.last_name, 'Ochieng')
        self.assertEqual(self.renter.email, 'mosesa.ochieng@gmail.com')
        self.assertEqual(self.renter.phone_number, '0701234568')
        self.assertEqual(self.renter.password, '')
        self.assertEqual(self.renter.username, 'Moses.Ochieng')

    def test_unique_email(self):
        # Create an initial borrower

        try:
            # Attempt to create a Renter with the same email
            Renters.objects.create(

                email='mosesa.ochieng@gmail.com',  # Same email as above

            )
            # If no exception is raised, the test should fail
            self.fail("IntegrityError not raised for duplicate email")
        except IntegrityError:
            # Expected outcome: IntegrityError should be raised
            pass
        except Exception as e:
            # Fail the test for any unexpected exception
            self.fail(f"Unexpected exception raised: {e}")

    def test_invalid_email_format(self):
        invalid_email_renter = Renters(

            first_name='Test',
            last_name='User',
            email='test.example.com',
            phone_number='1234567890',
            password='password123',
            username='testuser'  # Invalid email format
        )
        with self.assertRaises(ValidationError):
            invalid_email_renter.full_clean()

    def test_valid_email_format(self):
        valid_email_renter = Renters(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            password='password123',
            username='testuser'

        )
        try:
            valid_email_renter.full_clean()
        except ValidationError:
            self.fail("ValidationError raised for valid email format")


class RenterViewTests(APITestCase):
    def setUp(self):
        self.renter = Renters.objects.create(
            first_name='Moses',
            last_name='Ochieng',
            email='mosesa.ochieng@gmail.com',
            phone_number='0701234568',
            password='',
            username='Moses.Ochieng',
        )

        self.list_url = reverse('list')
        self.create_url = reverse('create')
        self.update_url = reverse('update', kwargs={'pk': self.renter.id})
        self.delete_url = reverse('delete', kwargs={'pk': self.renter.id})

    def test_create_renter(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone_number': '1234567890',
            'password': 'password123',
            'username': 'testuser'
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Renter created')
