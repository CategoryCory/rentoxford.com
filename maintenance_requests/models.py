from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class MaintenanceRequest(models.Model):
    PENDING = 'pending'
    RESOLVED = 'resolved'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (RESOLVED, 'Resolved'),
    )

    tenant = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Please provide a description of the maintenance problem you\'re '
                                                'having.')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=PENDING)
    service_provider_invoice = models.CharField(max_length=150, blank=True)
    resolution_notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tenant.first_name + ' ' + self.tenant.last_name + ' ' + str(self.created_on)

    def get_absolute_url(self):
        return reverse('maintenance_request_detail', args=[self.id])

    class Meta:
        verbose_name_plural = 'Maintenance Requests'
        ordering = ('-created_on', )
