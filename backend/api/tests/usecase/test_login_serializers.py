from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRFValidationError
from api.usecase.login.serializers import (
    UserSerializer,
    UserSerializerCreated,
    UserUpdateSerializer,
    UserLoginSerializer,
    UserLoginRefreshTokenSerializer
)

class UserSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')

    def test_user_serializer_valid(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'username', 'email', 'password']))
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertNotIn('password', data)

    def test_user_serializer_create(self):
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        serializer = UserSerializerCreated(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')

    def test_user_update_serializer_valid(self):
        data = {'username': 'updateduser', 'email': 'updated@example.com', 'password': 'newpassword'}
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertEqual(updated_user.username, 'updateduser')
        self.assertEqual(updated_user.email, 'updated@example.com')

    def test_user_login_serializer_valid(self):
        serializer = UserLoginSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'username', 'email', 'password']))
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)
        self.assertNotIn('password', data)

    def test_user_login_refresh_token_serializer_valid(self):
        serializer = UserLoginRefreshTokenSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'username', 'email']))
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['email'], self.user.email)

    def test_user_serializer_invalid(self):
        data = {'username': '', 'email': 'invalid-email', 'password': 'short'}
        serializer = UserSerializer(data=data)
        with self.assertRaises(DRFValidationError):
            serializer.is_valid(raise_exception=True)

    def test_user_update_serializer_invalid(self):
        data = {'username': '', 'email': 'invalid-email'}
        serializer = UserUpdateSerializer(instance=self.user, data=data, partial=True)
        with self.assertRaises(DRFValidationError):
            serializer.is_valid(raise_exception=True)
