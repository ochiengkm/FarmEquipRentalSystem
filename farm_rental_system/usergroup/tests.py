from django.test import TestCase


def test_initial():
    assert True


def test_failing():
    print("This is a message")
    assert 1 == 2

# Create your tests here.
