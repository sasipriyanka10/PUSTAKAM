from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='books/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('category/<int:pk>/', views.category_books, name='category_books'),
    
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('checkout/', views.checkout, name='checkout'),
    
    path('upload/', views.upload_book, name='upload_book'),
    path('my-books/', views.my_books, name='my_books'),
    
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:book_id>/', views.add_to_wishlist, name='add_to_wishlist'),
]
