import razorpay
import hmac
import hashlib
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Booking
from .serializers import BookingSerializer, RescheduleSerializer, PaymentConfirmSerializer

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

class BookingListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        price_paise = int(serializer.validated_data['price'] * 100)
        try:
            rz_order = razorpay_client.order.create({
                'amount':  price_paise,
                'currency': 'INR',
                'payment_capture': 1,
            })
        except Exception as e:
            return Response(
                {'error': f'Razorpay order creation failed: {str(e)}'},
                status=status.HTTP_502_BAD_GATEWAY
            )
        booking = serializer.save(
            user=request.user,
            razorpay_order_id=rz_order['id']
        )

        return Response({
            'booking_id': booking.id,
            'razorpay_order_id': rz_order['id'],
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'amount': price_paise,
            'currency': 'INR',
            'booking': BookingSerializer(booking).data,
        }, status=status.HTTP_201_CREATED)

class BookingDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Booking.objects.get(pk=pk, user=user)
        except Booking.DoesNotExist:
            return None

    def get(self, request, pk):
        booking = self.get_object(pk, request.user)
        if not booking:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BookingSerializer(booking).data)

    def delete(self, request, pk):
        booking = self.get_object(pk, request.user)
        if not booking:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        if booking.status == 'cancelled':
            return Response({'error': 'Booking is already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({'message': 'Booking cancelled successfully.'})

class BookingRescheduleView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'cancelled':
            return Response({'error': 'Cannot reschedule a cancelled booking.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RescheduleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_date      = serializer.validated_data['date']
        new_time      = serializer.validated_data['time_slot']
        holiday_shift = serializer.validated_data['is_holiday_shifted']
        clash = Booking.objects.filter(
            user=request.user, date=new_date,
            time_slot=new_time, status='confirmed'
        ).exclude(pk=pk)

        if clash.exists():
            return Response(
                {'error': 'You already have a booking at this new date and time.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.date  = new_date
        booking.time_slot = new_time
        booking.is_holiday_shifted = holiday_shift
        # Keep status as confirmed if payment was done, otherwise pending
        if booking.razorpay_payment_id:
            booking.status = 'confirmed'
        else:
            booking.status = 'pending'
        booking.save()

        return Response({
            'message': 'Booking rescheduled successfully.',
            'booking': BookingSerializer(booking).data,
        })

class PaymentConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_id   = serializer.validated_data['razorpay_order_id']
        payment_id = serializer.validated_data['razorpay_payment_id']
        signature  = serializer.validated_data['razorpay_signature']
        msg = f"{order_id}|{payment_id}".encode()
        expected = hmac.new(
            settings.RAZORPAY_KEY_SECRET.encode(),
            msg,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected, signature):
            return Response({'error': 'Invalid payment signature.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(
                razorpay_order_id=order_id,
                user=request.user
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found for this order.'}, status=status.HTTP_404_NOT_FOUND)

        booking.razorpay_payment_id = payment_id
        booking.status  = 'confirmed'
        booking.save()

        return Response({
            'message': 'Payment confirmed. Booking is active.',
            'booking': BookingSerializer(booking).data,
        })