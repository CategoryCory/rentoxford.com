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
        send_mail(
            'Submission from contact form',
            form.cleaned_data.get('message'),
            'admin@rentoxford.com',
            [settings.CONTACT_FORM_EMAIL_TO],
            fail_silently=False
        )
        return super().form_valid(form)


class CommunitiesPageView(TemplateView):
    template_name = 'pages/communities.html'
