from django.test import TestCase

# Create your tests here.

from django.contrib.auth.models import User
from django.forms import Field
from django.test import TestCase
from fotos.forms import RegisterUserForm


# Create your tests here.


class TestDataMixin:

    @classmethod
    def setup_test_data(cls):
        cls.u1 = User.objects.create_user(username='Andy',
                                          password='password',
                                          email='testclient@example.com')


class UserCreationFormTest(TestDataMixin, TestCase):

    def test_user_already_exists(self):
        user = User.objects.create_user('Andy',
                                        'testclient@example.com',
                                        'test123')
        data = {
            'username': 'Andy',
            'email': 'testclient@example.com',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = RegisterUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['username'].errors,
                         [str(User._meta.get_field('username').
                              error_messages['unique'])])

    def test_password_verification(self):
        # The verification password is incorrect.
        data = {
            'username': 'Andy',
            'password1': 'test123',
            'password2': 'test',
        }
        form = RegisterUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form["password2"].errors,
                         [str(form.error_messages['password_mismatch'])])

    def test_invalid_data(self):
        data = {
            'username': 'Andy!',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = RegisterUserForm(data)
        self.assertFalse(form.is_valid())
        validator = next(v for v in User.
                         _meta.get_field('username').
                         validators if v.code == 'invalid')
        self.assertEqual(form["username"].errors,
                         [str(validator.message)])

    def test_both_passwords(self):
        # One (or both) passwords weren't given
        data = {'username': 'Andy'}
        form = RegisterUserForm(data)
        required_error = [str(Field.default_error_messages['required'])]
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, required_error)

        data['password2'] = ''
        form = RegisterUserForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form['password1'].errors, required_error)
        self.assertEqual(form['password2'].errors, required_error)

    def test_unicode_username(self):
        data = {
            'username': '宝',
            'email': 'testclient@example.com',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = RegisterUserForm(data)
        self.assertTrue(form.is_valid())
        u = form.save()
        self.assertEqual(u.username, '宝')
