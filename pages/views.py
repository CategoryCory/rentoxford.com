from django.views.generic import TemplateView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy

from contacts.forms import ContactForm


class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class ContactPageView(SuccessMessageMixin, CreateView):
    form_class = ContactForm
    template_name = 'pages/contact.html'
    success_url = reverse_lazy('pages:contact')
    success_message = 'Thank you for contacting us! We will be in touch with you soon.'

    def form_valid(self, form):
        email_subject = 'Submission from RentOxford contact form'
        email_body = (
            f'There is a new submission from the contact form on RentOxford.com.\n'
            f'Name: {form.cleaned_data.get("name")}\n'
            f'Email Address: {form.cleaned_data.get("email_address")}\n'
            f'Phone Number: {form.cleaned_data.get("phone_number")}\n'
            f'Message: {form.cleaned_data.get("message")}'
        )
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [settings.CONTACT_FORM_EMAIL_TO],
            fail_silently=True
        )
        return super().form_valid(form)


class CommunitiesPageView(TemplateView):
    template_name = 'pages/communities.html'
