from django.contrib import admin
from .models import Car, Order, Contact, Review, Feedback


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
	list_display = ('car_name', 'price', 'car_id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('order_id', 'name', 'email', 'phone', 'date')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'phone_number')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('user', 'rating', 'created_at')
	search_fields = ('user__username', 'content')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'feedback_type', 'subject', 'status', 'created_at')
	list_filter = ('status', 'feedback_type', 'created_at')
	search_fields = ('user__username', 'subject', 'message')
	ordering = ('-created_at',)
