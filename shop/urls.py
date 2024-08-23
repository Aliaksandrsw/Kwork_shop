from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
app_name = 'shop'
urlpatterns = [
    path('', cache_page(30)(views.ProductListView.as_view()), name='product_list'),
    path('<slug:category_slug>/', cache_page(30)(views.ProductListView.as_view()), name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]