from django.urls import path

from .views import (
    IntegrationListCreateView,
    OAuthSimulationView,
)

urlpatterns = [
    path('', IntegrationListCreateView.as_view(), name='integration-list-create'),

    path(
        'oauth/simulate/',
        OAuthSimulationView.as_view(),
        name='oauth-simulate'
    ),
]