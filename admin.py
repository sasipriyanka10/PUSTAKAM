from django.contrib import admin
from .models import Category, Book, Review, Cart, CartItem, Order, OrderItem, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BookImageInline(admin.TabularInline):
    model = Book.images.rel.related_model
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'category', 'seller', 'condition', 'status')
    list_filter = ('category', 'condition', 'status')
    search_fields = ('title', 'author')
    list_editable = ('status',)
    inlines = [BookImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

admin.site.register(OrderItem) # Or inline in Order
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(CartItem)
