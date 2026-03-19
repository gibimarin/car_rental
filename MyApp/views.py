from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Car, Order, Contact
from django.contrib.admin.views.decorators import staff_member_required
from .models import Review
from django.contrib.auth.decorators import login_required


# Home page
def index(request):
    return render(request, 'index.html')


# About page
def about(request):
    return render(request, 'about.html')


# User Registration
def register(request):
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')

        # Check password match
        if password != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Create user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name = name
        myuser.save()
        messages.success(request, "Your account has been successfully created!")
        return redirect('signin')

    return render(request, 'register.html')


# User Signin
def signin(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, 'login.html')


# User Signout
def signout(request):
    logout(request)
    messages.success(request, "Successfully logged out!")
    return redirect('home')


# Vehicles Page
def vehicles(request):
    cars = Car.objects.all()
    return render(request, 'vehicles.html', {'cars': cars})


# Billing Page
def bill(request):
    cars = Car.objects.all()
    return render(request, 'bill.html', {'cars': cars})


# Order Submission
def order(request):
    if request.method == "POST":
        billname = request.POST.get('billname', '')
        billemail = request.POST.get('billemail', '')
        billphone = request.POST.get('billphone', '')
        billaddress = request.POST.get('billaddress', '')
        billcity = request.POST.get('billcity', '')
        cars11 = request.POST.get('cars11', '')
        dayss = request.POST.get('dayss', '')
        date = request.POST.get('date', '')
        fl = request.POST.get('fl', '')
        tl = request.POST.get('tl', '')

        # Save the order
        new_order = Order(
            name=billname,
            email=billemail,
            phone=billphone,
            address=billaddress,
            city=billcity,
            cars=cars11,
            days_for_rent=dayss,
            date=date,
            loc_from=fl,
            loc_to=tl
        )
        new_order.save()
        messages.success(request, "Order placed successfully!")
        return redirect('home')

    # GET request
    cars = Car.objects.all()
    return render(request, 'bill.html', {'cars': cars})


# Contact Page
def contact(request):
    if request.method == "POST":
        contactname = request.POST.get('contactname', '')
        contactemail = request.POST.get('contactemail', '')
        contactnumber = request.POST.get('contactnumber', '')
        contactmsg = request.POST.get('contactmsg', '')

        new_contact = Contact(
            name=contactname,
            email=contactemail,
            phone_number=contactnumber,
            message=contactmsg
        )
        new_contact.save()
        messages.success(request, "Your message has been sent successfully!")

    return render(request, 'contact.html')


# List all registered users
@staff_member_required
def register_list(request):
    users = User.objects.all()
    return render(request, 'register_list.html', {'users': users})
@login_required
def create_review(request):
    if request.method == "POST":
        content = request.POST.get('content', '')
        rating = request.POST.get('rating', 5)

        if content.strip():  # ensure content is not empty
            Review.objects.create(
                user=request.user,
                content=content,
                rating=rating
            )
            messages.success(request, "Your review has been submitted!")
        else:
            messages.error(request, "Review cannot be empty.")

        return redirect('reviews')  # redirect to reviews page

    return render(request, 'create_review.html')

# List all reviews
def reviews(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': all_reviews})

# Add these imports at the top of MyApp/views.py
from .models import Feedback # Add Feedback to the import from .models
from django.shortcuts import get_object_or_404
from .forms import FeedbackForm

# Add these new view functions to MyApp/views.py

@login_required
def submit_feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            fb = form.save(commit=False)
            fb.user = request.user
            fb.save()
            messages.success(request, "Thank you! Your feedback has been submitted successfully.")
            return redirect('home')
        else:
            # Form invalid - fall through to render with errors
            messages.error(request, "Please correct the errors below.")
    else:
        form = FeedbackForm()

    return render(request, 'submit-feedback.html', {'form': form})

@login_required
def view_my_feedback(request):
    """
    Allows a user to see the history and status of their own submissions.
    """
    user_feedback = Feedback.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'view_my_feedback.html', {'feedback_list': user_feedback})


@staff_member_required
def manage_feedback(request):
    """
    An admin-only view to see all feedback and update its status.
    """
    if request.method == "POST":
        feedback_id = request.POST.get("feedback_id")
        new_status = request.POST.get("status")
        try:
            feedback_item = get_object_or_404(Feedback, id=feedback_id)
            if new_status in dict(Feedback.STATUS_CHOICES):
                feedback_item.status = new_status
                feedback_item.save()
                messages.success(request, f"Status for feedback #{feedback_id} updated to '{new_status}'.")
            else:
                messages.error(request, "Invalid status value.")
        except Exception as e:
            messages.error(request, f"Could not update feedback: {e}")
        return redirect('manage_feedback')

    all_feedback = Feedback.objects.all().order_by('-created_at')
    return render(request, 'manage_feedback.html', {'feedback_list': all_feedback})

# Add this import at the top of MyApp/views.py
from django.db.models import Count

# Add this new view function to MyApp/views.py

@staff_member_required
def admin_dashboard(request):
    # Get key statistics
    total_users = User.objects.count()
    total_vehicles = Car.objects.count()
    total_orders = Order.objects.count()
    total_feedback = Feedback.objects.count()

    # Get recent data
    recent_orders = Order.objects.order_by('-order_id')[:5]  # Get the last 5 orders
    recent_users = User.objects.order_by('-date_joined')[:5]   # Get the last 5 users

    context = {
        'total_users': total_users,
        'total_vehicles': total_vehicles,
        'total_orders': total_orders,
        'total_feedback': total_feedback,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }
    return render(request, 'admin_dashboard.html', context)

# Add these imports at the top of MyApp/views.py
from .forms import CarForm

# Add this new view function
@staff_member_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'New car has been added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CarForm()

    return render(request, 'add_car.html', {'form': form})