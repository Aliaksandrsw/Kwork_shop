from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from cart.forms import CartAddProductForm
from .models import Category, Products


class ProductListView(ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    model = Products

    def get_queryset(self):
        queryset = Products.objects.filter(available=True)
        self.category = None

        if self.kwargs.get('category_slug'):
            self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            queryset = queryset.filter(category=self.category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category'] = self.category
        return context


class ProductDetailView(DetailView):
    model = Products
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_object(self):
        id_ = self.kwargs.get('id')
        slug = self.kwargs.get('slug')
        return get_object_or_404(Products, id=id_, slug=slug, available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        return context