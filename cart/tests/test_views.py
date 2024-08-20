from django.test import Client, TestCase
from django.urls import reverse
from decimal import Decimal
from shop.models import Products, Category
from cart.cart import Cart
from cart.forms import CartAddProductForm


class CartViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.product = Products.objects.create(name='Test Product', price=9.99, category=self.category,
                                               slug='test-product')


    def test_cart_add_view(self):
        response = self.client.post(reverse('cart:cart_add', args=[self.product.id]),
                                    data={'quantity': 2, 'override': False}, follow=True)
        cart = Cart(response.wsgi_request)
        self.assertEqual(len(cart), 2)
        cart_item = next(iter(cart))
        self.assertEqual(cart_item['product'], self.product)
        self.assertEqual(cart_item['quantity'], 2)
        self.assertEqual(cart_item['price'], Decimal('9.99'))

    def test_cart_remove_view(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), data={'quantity': 2, 'override': False})
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertContains(response, self.product.name)
        response = self.client.post(reverse('cart:cart_remove', args=[self.product.id]), follow=True)
        self.assertRedirects(response, reverse('cart:cart_detail'))
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertNotContains(response, self.product.name)

    def test_cart_detail_view(self):
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), data={'quantity': 2, 'override': False})
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertContains(response, self.product.name)
        self.assertContains(response, '2')
        self.assertContains(response, '<select name="quantity" id="id_quantity">')
        self.assertContains(response, '<input type="hidden" name="override" value="True" id="id_override">')
        self.assertContains(response, '<input type="submit" value="Update">')
