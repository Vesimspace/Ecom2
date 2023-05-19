from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('search', views.search, name="search"),
    path('categories/', views.categories, name="categories"),
    path('brands/', views.brands, name="brands"),
    path('products/', views.products, name="products"),
    path('product-list/<int:category_id>', views.product_list, name="product-list"),
    path('brand-product-list/<int:brand_id>', views.brand_product_list, name="brand-product-list"),
    path('product/<str:slug>/<int:id>', views.product_page, name='product_page'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('load-more-data', views.load_more_data, name='load_more_data'),
    path('add-to-cart', views.add_to_cart, name='add_to_cart'),
    path('cart', views.cart, name='cart'),
    path('delete-from-cart', views.delete_cart_item, name='delete_from_cart'),
    path('update-cart', views.update_cart_item, name='update-cart'),
    path('accounts/register', views.register, name='register'),
    path('checkout', views.checkout, name='checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_canceled, name='payment_cancelled'),
    path('save-review/<int:pid>',views.save_review, name='save-review'),
    path('dashboard', views.my_dashboard, name='dashboard'),
    path('orders', views.my_orders, name='orders'),
    path('order-items/<int:id>', views.my_order_items, name='order-items'), 
    path('wishlist', views.wishlist, name="wishlist"),
    path('my-wishlist', views.my_wishlist, name="my-wishlist"),
    path('reviews', views.reviews, name="reviews"),
    path('address', views.address, name="address"),
    path('save-address', views.save_address, name="save-address"),
    path('update-address/<int:id>', views.update_address, name="update-address"),
    path('activate-address', views.activate_address, name="activate-address"),
    path('profile', views.profile, name="profile"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)