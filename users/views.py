from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ActivateUserSerializer, RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ActivateUserView(APIView):
    @swagger_auto_schema(
        request_body=ActivateUserSerializer,
        responses={
            200: openapi.Response(
                description="Аккаунт успешно активирован",
                examples={"application/json": {"detail": "Аккаунт успешно активирован"}}
            ),
            400: openapi.Response(
                description="Неверный код или email",
                examples={"application/json": {"detail": "Неверный email или код активации"}}
            )
        }
    )
    def post(self, request):
        serializer = ActivateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['activation_code']

        try:
            user = Client.objects.get(email=email, activation_code=code, is_active=False)
        except Client.DoesNotExist:
            return Response(
                {"detail": "Неверный email или код активации"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.activation_code = None
        user.save(update_fields=['is_active', 'activation_code'])

        return Response(
            {"detail": "Аккаунт успешно активирован"},
            status=status.HTTP_200_OK
        )
    
class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response(
                description="Пользователь успешно зарегистрирован",
                examples={"application/json": {"detail": "Проверьте почту для активации аккаунта"}},
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Проверьте почту для активации аккаунта"},
            status=status.HTTP_201_CREATED,
        )
