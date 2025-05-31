# newbrand/views.py
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
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


def contact_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        # 여기에 이메일 전송 로직 또는 DB 저장 로직을 추가
        # 예: send_mail(subject, message, email, ['support@newbrand.com'])

        messages.success(
            request, "문의가 성공적으로 전송되었습니다! 빠르게 회신드리겠습니다."
        )
        return redirect("newbrand:contact")
    return redirect("newbrand:contact")
