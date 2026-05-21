from rest_framework import serializers
from .models import *
from decimal import Decimal

PLAN_PRICES = {
    'basic':           Decimal('300.00'),
    'monthly_premium': Decimal('2400.00'),
    'custom':          Decimal('300.00'),
}

class BookingSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source = 'user.email', read_only = True)
    user_name  = serializers.CharField(source='user.full_name', read_only=True)


    class  Meta:
        model = Booking
        fields = [
            'id', 'user_email', 'user_name',
            'plan', 'date', 'time_slot',
            'slots_count', 'price', 'status',
            'is_holiday_shifted',
            'razorpay_order_id', 'razorpay_payment_id',
            'created_at',
        ]

        read_only_fields = [
            'id', 'price', 'status',
            'razorpay_order_id', 'razorpay_payment_id',
            'created_at', 'user_email', 'user_name',
        ]

    def validate_slots_count(self, value):
            
            if value < 1:
                raise serializers.ValidationError("Slots count must be atleast 1. ")
            return value
        

    def validate(self, data):
            plan = data.get('plan')
            date  = data.get('date')
            time_slot = data.get('time_slot')
            slots_count = data.get('slots_count', 1)
            user = self.context['request'].user


            if plan == 'basic':
                data['slots_count'] = 1
            elif plan == 'monthly_premium':
                data['slots_count'] = 8

            ab = Booking.objects.filter(
                user = user,date=date, time_slot=time_slot, status='confirmed'
            )
            if self.instance:
                ab = ab.exclude(pk=self.instance.pk)

            if ab.exists():
                raise serializers.ValidationError("You already have a confirmed booking at this date and time. ")
            

            if plan == 'custom':
                data['price'] = PLAN_PRICES['custom'] * slots_count
            else:
                data['price'] = PLAN_PRICES[plan]

            return data
        
class RescheduleSerializer(serializers.Serializer):
    date = serializers.DateField()
    time_slot = serializers.TimeField()
    is_holiday_shifted = serializers.BooleanField(default=False)


 
class PaymentConfirmSerializer(serializers.Serializer):
    razorpay_order_id   = serializers.CharField()
    razorpay_payment_id = serializers.CharField()
    razorpay_signature  = serializers.CharField()