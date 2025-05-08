from django.urls import path
from . import views
from . import payment_views

app_name = 'store'
urlpatterns = [
    # Existing views
    path('use_<int:use>', views.index, name='store'),
    
    # Payment views
    path('product/<int:product_id>/', payment_views.product_detail, name='product_detail'),
    path('checkout/<int:product_id>/', payment_views.create_checkout_session, name='create_checkout'),
    path('payment/success/', payment_views.payment_success, name='payment_success'),
    path('payment/cancel/', payment_views.payment_cancel, name='payment_cancel'),
    path('payment/failed/', payment_views.payment_failed, name='payment_failed'),
    path('order/success/<int:order_id>/', payment_views.order_success, name='order_success'),
    path('webhook/stripe/', payment_views.stripe_webhook, name='stripe_webhook'),
    path('my-purchases/', payment_views.my_purchases, name='my_purchases'),
    path('add-product/', views.add_product, name='add_product'),
]