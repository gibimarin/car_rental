from django.contrib import admin
from django.urls import path
from MyApp import views
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    path("", views.index, name='home'),
    path("home", views.index, name='home'),
    path("about", views.about, name='about'),
    path("vehicles", views.vehicles, name="vehicles"),
    path("register", views.register, name="register"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("bill", views.order, name="bill"),
    path("contact", views.contact, name='contact'),
    path('reviews/', views.reviews, name='reviews'),
    path('create-review/', views.create_review, name='create_review'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('feedback/my-feedback/', views.view_my_feedback, name='view_my_feedback'),
    path('feedback/manage/', views.manage_feedback, name='manage_feedback'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # 🚗 New admin features
    
    path('register-list/', views.register_list, name='register_list'),
    # avoid using the 'admin/' prefix which collides with Django's admin app
    path('adminpanel/add-car/', views.add_car, name='add_car'),
    # keep a redirect from the old admin path to the new one to avoid 404s from cached links
    path('admin/add-car/', RedirectView.as_view(url='/adminpanel/add-car/', permanent=True)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)