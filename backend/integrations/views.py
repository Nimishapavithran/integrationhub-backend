from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Integration
from .serializers import IntegrationSerializer


class IntegrationListCreateView(generics.ListCreateAPIView):

    serializer_class = IntegrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Integration.objects.filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from rest_framework.views import APIView
from rest_framework.response import Response

from .services.oauth_service import OAuthService


class OAuthSimulationView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        provider = request.data.get("provider")

        access_token = OAuthService.generate_access_token()

        refresh_token = OAuthService.generate_refresh_token()

        integration = Integration.objects.create(
            user=request.user,
            provider=provider,
            access_token=access_token,
            refresh_token=refresh_token,
            realm_id="simulated-company-id"
        )

        serializer = IntegrationSerializer(integration)

        return Response(serializer.data)        