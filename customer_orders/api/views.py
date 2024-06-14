from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Customer, Order
from .serializers import CustomerSerializer, OrderSerializer
from .tasks import send_order_alert

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save()
        send_order_alert(order.customer, order)

