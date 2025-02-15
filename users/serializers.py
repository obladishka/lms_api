from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from users.models import Payment, User


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Payment",
            value={
                "id": 0,
                "payment_date": "2019-08-24T14:15:22Z",
                "payment_amount": 100.25,
                "payment_method": "cash",
                "user": 0,
                "course": 0,
                "lesson": 0,
            },
            response_only=True,
        ),
    ]
)
class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "city",
            "avatar",
            "payments",
        )


class UserBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "city",
            "avatar",
        )
