from django.test import TestCase
from cart.forms import CartAddProductForm

class TestCartAddProductForm(TestCase):
    def test_form_valid_data(self):
        """Test the form with valid data"""
        data = {
            'quantity': '5',
            'override': 'False',
        }
        form = CartAddProductForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['quantity'], 5)
        self.assertEqual(form.cleaned_data['override'], False)

    def test_form_missing_quantity(self):
        """Test the form with missing quantity"""
        data = {
            'override': 'False',
        }
        form = CartAddProductForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_form_invalid_quantity(self):
        """Test the form with invalid quantity"""
        data = {
            'quantity': '0',
            'override': 'False',
        }
        form = CartAddProductForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_form_override_field(self):
        """Test the override field"""
        data = {
            'quantity': '5',
            'override': 'True',
        }
        form = CartAddProductForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['override'], True)