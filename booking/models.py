from django.db import models
from django.conf import settings

PLAN_CHOICES = [
    ('basic', 'Basic'),
    ('monthly_premium', 'Monthly Premium'),
    ('custom', 'Custom'),

]

STATUS_CHOICES = [
    ('confirmed', 'Confirmed'),
    ('rescheduled', 'Rescheduled'),
    ('cancelled', 'Cancelled'),
    ('pending', 'Pending')

]

class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES)
    date = models.CharField()
    time_slot = models.TimeField()
    slots_count = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')
    is_holiday_shifted = models.BooleanField(default=False)
    razorpay_order_id  = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id= models.CharField(max_length=100, blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} | {self.plan} | {self.date} {self.time_slot}"

# Create your models here.
