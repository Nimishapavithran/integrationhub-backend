from celery import shared_task

from .models import Integration

import time


@shared_task
def sync_user_integrations(user_id):

    integrations = Integration.objects.filter(
        user_id=user_id
    )

    print(f"Found {integrations.count()} integrations")

    for integration in integrations:

        print(f"Syncing {integration.provider}")

        time.sleep(3)

    return "All integrations synced"