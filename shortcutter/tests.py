import faker
import pytest

from rest_framework.test import APIClient

from .models import ShortURLModel
from .utils import get_short_code
from users.models import User

fake = faker.Faker()


@pytest.fixture(scope="function")
def api_client_anonymous():
    yield APIClient()


@pytest.fixture(scope="function")
def api_client_with_user():
    user, _ = User.objects.get_or_create(
        username="user_test_1",
        first_name="First_test",
        last_name="Last_test",
        password="user_test_1!",
        email="test@mail.ru",
    )
    api_client = APIClient()
    api_client.force_authenticate(user)
    yield api_client


@pytest.mark.django_db
def test_create_anonymous_short_url_without_alias(api_client_anonymous: APIClient):
    """
    Test for creation anonymous short_url

    Args:
        api_client (APIClient): The object for API imitation

    Returns:
        None
    """

    data_for_creating = {"full_url": fake.url()}
    path = "/shortcutter/short_url/"

    response = api_client_anonymous.post(path=path, data=data_for_creating)

    assert response.status_code == 201
    assert response.data["full_url"] == data_for_creating["full_url"]
    assert response.data["short_code"] is not None
    assert response.data["author"] is None


@pytest.mark.django_db
def test_create_anonymous_short_url_with_alias(api_client_anonymous: APIClient):
    """
    Test for creation anonymous short_url with custom alias

    Args:
        api_client (APIClient): The object for API imitation

    Returns:
        None
    """

    data_for_creating = {"full_url": fake.url(), "alias": "test12"}
    path = "/shortcutter/short_url/"

    response = api_client_anonymous.post(path=path, data=data_for_creating)

    assert response.status_code == 201
    assert response.data["full_url"] == data_for_creating["full_url"]
    assert response.data["short_code"] == data_for_creating["alias"]
    assert response.data["author"] is None


@pytest.mark.django_db
def test_create_short_url_without_alias(api_client_with_user: APIClient):
    """
    Test for creation short_url by user

    Args:
        api_client_with_user (APIClient): The object for API imitation

    Returns:
        None
    """
    user = User.objects.get(username="user_test_1")

    data_for_creating = {"full_url": fake.url()}
    path = "/shortcutter/short_url/"

    response = api_client_with_user.post(path=path, data=data_for_creating)

    assert response.status_code == 201
    assert response.data["full_url"] == data_for_creating["full_url"]
    assert response.data["short_code"] is not None
    assert response.data["author"] == user.uuid


@pytest.mark.django_db
def test_create_short_url_with_alias(api_client_with_user: APIClient):
    """
    Test for creation short_url by user with user's alias

    Args:
        api_client_with_user (APIClient): The object for API imitation

    Returns:
        None
    """
    user = User.objects.get(username="user_test_1")

    data_for_creating = {"full_url": fake.url(), "alias": "alias2"}
    path = "/shortcutter/short_url/"

    response = api_client_with_user.post(path=path, data=data_for_creating)

    assert response.status_code == 201
    assert response.data["full_url"] == data_for_creating["full_url"]
    assert response.data["short_code"] == data_for_creating["alias"]
    assert response.data["author"] == user.uuid


@pytest.mark.django_db
def test_redirect(api_client_anonymous: APIClient, mocker):
    """
    Test for redirection

    Args:
        api_client_anonymous (APIClient): The object for API imitation

    Returns:
        None
    """
    short_url, _ = ShortURLModel.objects.get_or_create(
        full_url=fake.url(), short_code=get_short_code()
    )

    path = f"/{short_url.short_code}"

    response = api_client_anonymous.get(path=path)

    assert response.status_code == 302
