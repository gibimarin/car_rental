from email.policy import default
from django.db import models

from django.contrib.auth.models import User

class Car(models.Model):
    car_id = models.IntegerField(default=0)
    car_name = models.CharField(max_length=30,default="")
    car_desc = models.CharField(max_length=300,default="")
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="car/images",default="")

    def __str__(self):
        return self.car_name

class Order(models.Model) :
    order_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=90,default="")
    email = models.CharField(max_length=50,default="")
    phone = models.CharField(max_length=20,default="")
    address = models.CharField(max_length=500,default="")
    city = models.CharField(max_length=50,default="")
    cars = models.CharField(max_length=50,default="")
    days_for_rent = models.IntegerField(default=0)
    date = models.CharField(max_length=50,default="")
    loc_from = models.CharField(max_length=50,default="")
    loc_to = models.CharField(max_length=50,default="")
    
    def __str__(self):
        return self.name

class Contact(models.Model):
    message = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150,default="")
    email = models.CharField(max_length=150,default="")
    phone_number = models.CharField(max_length=15,default="")
    message = models.TextField(max_length=500,default="")

    def __str__(self) :
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField("Review")
    rating = models.PositiveIntegerField(default=5)  # optional rating out of 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}/5"
    
# Add this to your MyApp/models.py file

class Feedback(models.Model):
    """
    Model to store user feedback, complaints, or suggestions.
    """
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    FEEDBACK_TYPE_CHOICES = [
        ('Complaint', 'Complaint'),
        ('Feedback', 'Feedback'),
        ('Suggestion', 'Suggestion'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_TYPE_CHOICES, default='Feedback')
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')

    def __str__(self):
        return f"{self.get_feedback_type_display()} from {self.user.username} - Status: {self.status}"