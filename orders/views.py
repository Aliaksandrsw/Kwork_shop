from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.shortcuts import render, redirect


class OrderCreateView(FormView):
    template_name = 'orders/order/create.html'
    form_class = OrderCreateForm
    success_url = reverse_lazy('order_created')

    def form_valid(self, form):
        cart = Cart(self.request)
        order = form.save()
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )
        cart.clear()
        order_created.delay(order.id)
        self.request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context['cart'] = cart
        return context
