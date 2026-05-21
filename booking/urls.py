from django.urls import path
from .views import *


urlpatterns = [
    # List all bookings / Create new booking
    path('', BookingListCreateView.as_view(), name='booking-list-create'),
 
    # Get single booking / Cancel booking
    path('<int:pk>/',BookingDetailView.as_view(),name='booking-detail'),
 
    # Reschedule booking (PATCH)
    path('<int:pk>/reschedule/', BookingRescheduleView.as_view(), name='booking-reschedule'),
 
    # Confirm payment after Razorpay checkout
    path('confirm-payment/', PaymentConfirmView.as_view(), name='booking-confirm-payment'),
]