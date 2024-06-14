from django.test import TestCase
from rest_framework.test import APIClient
from .models import Customer, Order

class CustomerOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer = Customer.objects.create(name='John Doe', code='1234')
        self.order = Order.objects.create(item='Test Item', amount=100, customer=self.customer)

    def test_create_customer(self):
        response = self.client.post('/api/customers/', {'name': 'Jane Doe', 'code': '5678'})
        self.assertEqual(response.status_code, 201)

    def test_create_order(self):
        response = self.client.post('/api/orders/', {'item': 'Another Item', 'amount': 50, 'customer': self.customer.id})
        self.assertEqual(response.status_code, 201)

