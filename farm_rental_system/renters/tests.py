import unittest

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from borrowers.models import Borrowers


class BorrowersModelTest(TestCase):
    def setUp(self):
        # Create an initial borrower with a specific email
        self.borrower = Borrowers.objects.create(
            first_name='Jescah',
            last_name='Anyangu',
            email='jessy@gmail.com',
            phone_number='079071925',
            password='',
            username='Jescah.Anyangu',
        )

    def test_borrower_creation(self):
        self.assertEqual(self.borrower.first_name, 'Jescah')
        self.assertEqual(self.borrower.last_name, 'Anyangu')
        self.assertEqual(self.borrower.email, 'jessy@gmail.com')
        self.assertEqual(self.borrower.phone_number, '079071925')
        self.assertEqual(self.borrower.password, '')
        self.assertEqual(self.borrower.username, 'Jescah.Anyangu')

    def test_unique_email(self):
        # Create an initial borrower

        try:
            # Attempt to create a borrower with the same email
            Borrowers.objects.create(

                email='jessy@gmail.com',  # Same email as above

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
        invalid_email_borrower = Borrowers(

            first_name='Test',
            last_name='User',
            email='test.example.com',
            phone_number='1234567890',
            password='password123',
            username='testuser'  # Invalid email format
        )
        with self.assertRaises(ValidationError):
            invalid_email_borrower.full_clean()

    def test_valid_email_format(self):
        valid_email_borrower = Borrowers(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone_number='1234567890',
            password='password123',
            username='testuser'

        )
        try:
            valid_email_borrower.full_clean()
        except ValidationError:
            self.fail("ValidationError raised for valid email format")


class BorrowersViewTests(APITestCase):
    def setUp(self):
        self.borrower = Borrowers.objects.create(
            first_name='Jescah',
            last_name='Anyangu',
            email='jessy@gmail.com',
            phone_number='079071925',
            password='',
            username='Jescah.Anyangu',
        )

        self.list_url = reverse('list')
        self.create_url = reverse('create')
        self.update_url = reverse('update', kwargs={'pk': self.borrower.id})
        self.delete_url = reverse('delete', kwargs={'pk': self.borrower.id})

    def test_create_borrower(self):
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
        self.assertEqual(response.data['message'], 'Borrower created')
