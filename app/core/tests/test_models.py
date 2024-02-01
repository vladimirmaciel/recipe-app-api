"""
Tests for models.
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """ Create and return a new user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test model class"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'teste@mail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        # self.assertEqual(user.password, password)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email(self):
        """ user email is required """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='senha_supersecreta'
        )

        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.email, 'admin@example.com')

    def test_create_recipe(self):
        """ teste create recipe is successful"""
        user = get_user_model().objects.create_user(
            'test@mail.com',
            'testpass123',
        )

        """Test creating a new recipe"""
        recipe = models.Recipe.objects.create(
            user=user,
            title='Test recipe',
            time_minutes=5,
            price=Decimal('10.00'),
            description='Test description',
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful"""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_ingredient(self):
        """Test creating an ingredient is successful"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1')

        self.assertEqual(str(ingredient), ingredient.name)
