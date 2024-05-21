from datetime import datetime, timedelta

import pytest
from unittest.mock import patch

from apps.image_tickets.models import Ticket
from apps.image_tickets.types import (
    CreateTicketSuccessResponse,
    UploadImageSuccessResponse,
)

from rest_framework import status

from apps.utils.common.types import GeneralErrorResponse


endpoint = "/tickets"


def test_create_ticket_endpoint_should_return_201_status_when_ticket_creation_was_successful(
    client, user
):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    response = client.post(
        f"{endpoint}",
        {
            "max_image_quantity": 2,
        },
        format="json",
    )
    assert isinstance(response, CreateTicketSuccessResponse)
    assert response.status_code == status.HTTP_201_CREATED
    assert "ticket" in response.json()
    assert "max_image_quantity" in response.json()["ticket"]
    assert "status" in response.json()["ticket"]
    assert "created_by" in response.json()["ticket"]
    assert response.json()["ticket"]["max_image_quantity"] == 2
    assert response.json()["ticket"]["status"] == "PENDING"
    assert response.json()["ticket"]["created_by"] == user.id
    assert response.json()["ticket"]["loaded_image_quantity"] == 0


def test_create_ticket_endpoint_should_return_400_status_when_invalid_form(auth_client):
    response = auth_client.post(f"{endpoint}", {}, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response, GeneralErrorResponse)


def test_create_ticket_endpoint_should_return_403_status_when_user_not_authenticated(
    client,
):
    response = client.post(f"{endpoint}", {}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Authentication credentials were not provided."
    }


def test_get_paginated_tickets_endpoint_should_return_200_status_when_tickets_found(
    auth_client,
):
    response = auth_client.get(f"{endpoint}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_paginated_tickets_should_return_pending_status_tickets_when_status_filter_provided(
    client, user
):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    Ticket.objects.create(
        status="PENDING", created_by=user, max_image_quantity=2, loaded_image_quantity=0
    )
    Ticket.objects.create(
        status="COMPLETED",
        created_by=user,
        max_image_quantity=2,
        loaded_image_quantity=0,
    )
    response = client.get(f"{endpoint}", {"status": "PENDING"})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["status"] == "PENDING"
    assert response.data[0]["created_by"] == user.id
    assert response.data[0]["loaded_image_quantity"] == 0
    assert response.data[0]["max_image_quantity"] == 2


@pytest.mark.django_db
def test_get_paginated_tickets_should_return_tickets_in_timeframe_when_date_filters_are_provided(
    client, user
):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    Ticket.objects.create(  ## Move to ticket factory
        status="PENDING",
        created_by=user,
        max_image_quantity=2,
        loaded_image_quantity=0,
        created_at=datetime.now() - timedelta(days=2),
    )
    Ticket.objects.create(
        status="PENDING",
        created_by=user,
        max_image_quantity=2,
        loaded_image_quantity=0,
        created_at=datetime.now() - timedelta(days=1),
    )
    start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    response = client.get(
        f"{endpoint}", {"start_date": start_date, "end_date": end_date}
    )
    assert response.status_code == 200
    assert len(response.data) == 1


def test_get_paginated_ticket_should_return_403_status_when_user_not_authenticated(
    client,
):
    response = client.get(f"{endpoint}")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "Authentication credentials were not provided."
    }


@pytest.mark.django_db
def test_should_return_paginated_ticket_when_page_and_per_page_filters_are_provided(
    client, user
):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    Ticket.objects.create(
        status="PENDING", created_by=user, max_image_quantity=2, loaded_image_quantity=0
    )
    Ticket.objects.create(
        status="PENDING", created_by=user, max_image_quantity=2, loaded_image_quantity=0
    )
    response = client.get(f"{endpoint}", {"page": 1, "per_page": 1})
    assert response.status_code == 200
    assert len(response.data) == 1
