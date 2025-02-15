from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import Payment, User
from users.permissions import IsUser
from users.serializers import PaymentSerializer, UserBaseSerializer, UserSerializer
from users.services import create_price, get_payment_link


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data.get("password"))
        user.is_active = True
        user.save()


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUser,)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.kwargs.get("pk") == self.request.user.pk:
            return UserSerializer
        return UserBaseSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsUser,)


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        if request.data.get("payment_method") != "cash":
            amount = request.data.get("payment_amount")
            price = create_price(amount)
            payment_link = get_payment_link(price)
            return Response(
                {
                    "user": request.user.pk,
                    "course": request.data.get("course"),
                    "lesson": request.data.get("lesson"),
                    "payment_amount": request.data.get("payment_amount"),
                    "payment_method": request.data.get("payment_method"),
                    "payment_link": payment_link,
                }
            )

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment.save()
