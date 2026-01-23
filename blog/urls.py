from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('buy-coffee/', views.buy_coffee_view, name='buy_coffee'),
    path('buy-coffee/initiate/', views.initiate_payment, name='initiate_payment'),
    path('buy-coffee/verify/', views.verify_payment, name='verify_payment'),
    path('buy-coffee/fail/', views.payment_failed, name='payment_failed'),
    path('update-projects/', views.update_projects_webhook, name='update_projects_webhook'),
]
