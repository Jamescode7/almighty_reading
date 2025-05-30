# newbrand/views.py
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "newbrand/home.html"
    extra_context = {"title": "NEWBRAND | Home"}


class AboutView(TemplateView):
    template_name = "newbrand/about.html"
    extra_context = {"title": "About | NEWBRAND"}


class ProductView(TemplateView):
    template_name = "newbrand/product.html"
    extra_context = {"title": "Products | NEWBRAND"}


class ContactView(TemplateView):
    template_name = "newbrand/contact.html"
    extra_context = {"title": "Contact | NEWBRAND"}
