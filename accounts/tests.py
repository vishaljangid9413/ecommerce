from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import User

class UserModelTest(TestCase):

    def setUp(self):
        # Create a valid user
        self.valid_user = User.objects.create_user(
            name="John Doe",
            email="john.doe@example.com",
            mobile=9876543215,
            password="password123"
        )

    def test_user_creation(self):
        # Check if the user is created correctly
        user = self.valid_user
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertEqual(user.mobile, 9876543215)
        self.assertTrue(user.check_password("password123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_deleted)
        self.assertEqual(str(user), user.email)  # Verify the string representation

    def test_invalid_name(self):
        with self.assertRaises(ValidationError):
            invalid_user = User.objects.create_user(
                name="John123",  # Invalid name
                email="john.invalid@example.com",
                mobile=9876543216,
                password="password123"
            )
            invalid_user.full_clean() 

    def test_invalid_mobile(self):
        with self.assertRaises(ValidationError):
            invalid_user = User.objects.create_user(
                name="Jane Doe",
                email="jane.doe@example.com",
                mobile=12345, 
                password="password123"
            )
            invalid_user.full_clean() 

    def test_is_deleted_field(self):
        # Test the `is_deleted` field
        user = User.objects.create_user(
            name="Deleted User",
            email="deleted.user@example.com",
            mobile=9876543213,
            password="password123",
            is_deleted=True
        )
        self.assertTrue(user.is_deleted)  # `is_deleted` should be True

    def test_required_fields(self):
        # Ensure that email and mobile are required
        with self.assertRaises(TypeError):
            User.objects.create_user(
                name="Missing Fields User",
                password="password123"
            )

        # Test that creating a user with only required fields works (without `name`)
        user = User.objects.create_user(
            mobile=9876543214,
            email="no.name@example.com",
            password="password123"
        )
        self.assertEqual(user.email, "no.name@example.com")
        self.assertEqual(user.mobile, 9876543214)
