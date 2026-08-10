from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Book, Category, Cart, CartItem, Order, OrderItem, Review, Wishlist, BookImage
from .forms import RegistrationForm, BookForm, ReviewForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'books/register.html', {'form': form})

def about(request):
    return render(request, 'books/about.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Message sent! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'books/contact.html')

def home(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    
    if query:
        # If searching, show matching books
        featured_books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query),
            status='Approved'
        )
        recent_books = Book.objects.none() # Hide recent section slightly or just show results
        search_mode = True
    else:
        # Default view
        featured_books = Book.objects.filter(status='Approved', condition='New')[:4]
        recent_books = Book.objects.filter(status='Approved').order_by('-created_at')[:8]
        search_mode = False

    return render(request, 'books/home.html', {
        'categories': categories, 
        'featured_books': featured_books,
        'recent_books': recent_books,
        'search_query': query,
        'search_mode': search_mode
    })

def category_books(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category, status='Approved')
    return render(request, 'books/category_books.html', {'category': category, 'books': books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added!')
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    
    return render(request, 'books/book_detail.html', {'book': book, 'reviews': reviews, 'form': form})

@login_required
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            messages.success(request, 'Book uploaded successfully! Waiting for approval.')
            return redirect('my_books')
    else:
        form = BookForm()
    return render(request, 'books/upload.html', {'form': form})

@login_required
def my_books(request):
    books = Book.objects.filter(seller=request.user)
    return render(request, 'books/my_books.html', {'books': books})

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'books/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Added to cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            address=request.POST.get('address'),
            total_amount=cart.total_price
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('home') # Or order tracking page
    return render(request, 'books/checkout.html', {'cart': cart})

@login_required
def wishlist_view(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'books/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.books.add(book)
    messages.success(request, 'Added to wishlist!')
    return redirect('wishlist')
