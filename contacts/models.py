from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Contact Us Response'
        verbose_name_plural = 'Contact Us Responses'

    def __str__(self):
        return self.name
