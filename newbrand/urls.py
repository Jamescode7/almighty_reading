# newbrand/urls.py

from django.urls import path

from . import views

app_name = "newbrand"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("product/", views.ProductView.as_view(), name="product"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("contact/submit/", views.contact_submit, name="contact_submit"),
]
