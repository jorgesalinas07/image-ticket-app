from apps.image_tickets.types import CreateTicketSuccessResponse

from rest_framework import status

from apps.utils.common.types import GeneralErrorResponse


endpoint = '/tickets'

def test_create_ticket_endpoint_should_return_201_status_when_ticket_creation_was_successful(
    client, user
):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION='token ' + token.key)
    response = client.post(
        f'{endpoint}/',
        {
            'number_of_images': 2,
        },
        format='json',
    )
    assert isinstance(response, CreateTicketSuccessResponse)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'ticket' in response.json()
    assert 'number_of_images' in response.json()["ticket"]
    assert 'status' in response.json()["ticket"]
    assert 'created_by' in response.json()["ticket"]
    assert response.json()['ticket']['number_of_images'] == 2
    assert response.json()['ticket']['status'] == 'PENDING'
    assert response.json()['ticket']['created_by'] == user.id

def test_create_ticket_endpoint_should_return_400_status_when_invalid_form(client, user):
    user, token = user
    client.credentials(HTTP_AUTHORIZATION='token ' + token.key)
    response = client.post(f'{endpoint}/', {}, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert isinstance(response, GeneralErrorResponse)

def test_create_ticket_endpoint_should_return_403_status_when_user_not_authenticated(client):
    response = client.post(f'{endpoint}/', {}, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {'detail': 'Authentication credentials were not provided.'}
