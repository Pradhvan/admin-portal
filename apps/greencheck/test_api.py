import ipaddress
import logging

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import serializers
from rest_framework.authtoken import models, views
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory, RequestsClient

from apps.greencheck.models import GreencheckIp, Hostingprovider
from apps.greencheck.viewsets import IPRangeViewSet

User = get_user_model()

pytestmark = pytest.mark.django_db

logger = logging.getLogger(__name__)

rf = APIRequestFactory()


@pytest.mark.only
class TestUsingAuthToken:
    def test_fetching_auth_token(
        self, hosting_provider: Hostingprovider, sample_hoster_user: User,
    ):
        """
        Anyone who is able to update an organisation is able to
        generate an API token.
        """
        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()

        # set up our views, request factories and paths
        rf = APIRequestFactory()
        url_path = reverse("api-obtain-token")
        view = views.ObtainAuthToken.as_view()

        # create our request
        credentials = {"username": sample_hoster_user.username, "password": "topSekrit"}
        request = rf.post(url_path, credentials)

        response = view(request)
        token = models.Token.objects.get(user=sample_hoster_user)

        # check contents, is the token the right token?
        assert response.status_code == 200
        assert response.data["token"] == token.key


class TestIpRangeViewSetList:
    def test_get_ip_ranges_empty(
        self, hosting_provider: Hostingprovider, sample_hoster_user: User,
    ):
        """
        Exercise the simplest happy path.
        """

        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()

        rf = APIRequestFactory()
        url_path = reverse("ip-range-list")
        request = rf.get(url_path)
        request.user = sample_hoster_user

        # GET end point for IP Ranges
        view = IPRangeViewSet.as_view({"get": "list"})

        response = view(request)

        # check contents
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_get_ip_ranges_for_hostingprovider_with_active_range(
        self,
        hosting_provider: Hostingprovider,
        sample_hoster_user: User,
        green_ip: GreencheckIp,
    ):

        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()

        rf = APIRequestFactory()
        url_path = reverse("ip-range-list")
        request = rf.get(url_path)
        request.user = sample_hoster_user

        # GET end point for IP Ranges
        view = IPRangeViewSet.as_view({"get": "list"})

        response = view(request)
        ip_range, *_ = response.data

        assert response.status_code == 200
        assert len(response.data) == 1

        assert ip_range["ip_start"] == green_ip.ip_start
        assert ip_range["ip_end"] == green_ip.ip_end
        assert ip_range["hostingprovider"] == green_ip.hostingprovider.id
        assert ip_range["active"] == green_ip.active

    def test_get_ip_ranges_without_auth(
        self, hosting_provider: Hostingprovider, sample_hoster_user: User,
    ):
        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()

        rf = APIRequestFactory()
        url_path = reverse("ip-range-list")
        request = rf.get(url_path)

        # set up the viewset, as a views, so it knows what to do when we
        # pass in a GET request as defined a couple of lines up
        view = IPRangeViewSet.as_view({"get": "list"})

        # ipdb.set_trace()
        # has_permission = permission.has_permission(request, None)
        # import ipdb

        # ipdb.set_trace()
        response = view(request)

        # check contents
        assert response.status_code == 403
        # assert len(response.data) == 0

    def test_get_ip_range_for_user_with_no_hosting_provider(
        self, sample_hoster_user: User, rf: RequestFactory,
    ):
        sample_hoster_user.save()

        rf = APIRequestFactory()
        url_path = reverse("ip-range-list")
        request = rf.get(url_path)
        request.user = sample_hoster_user

        # GET end point for IP Ranges
        view = IPRangeViewSet.as_view({"get": "list"})
        response = view(request)

        # check contents
        assert response.status_code == 200
        assert len(response.data) == 0


class TestIpRangeViewSetRetrieve:
    """
    Can we fetch a specific IP Range object to inspect?
    """

    def test_get_ip_range_for_hostingprovider_by_id(
        self,
        hosting_provider: Hostingprovider,
        sample_hoster_user: User,
        green_ip: GreencheckIp,
    ):

        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()

        rf = APIRequestFactory()
        url_path = reverse("ip-range-detail", kwargs={"pk": green_ip.id})
        request = rf.get(url_path)
        request.user = sample_hoster_user

        # GET end point for IP Ranges
        view = IPRangeViewSet.as_view({"get": "retrieve"})

        response = view(request, pk=green_ip.id)

        assert response.status_code == 200

        assert response.data["ip_start"] == green_ip.ip_start
        assert response.data["ip_end"] == green_ip.ip_end
        assert response.data["hostingprovider"] == green_ip.hostingprovider.id
        assert response.data["active"] == green_ip.active


@pytest.mark.only
class TestIpRangeViewSetCreate:
    def test_create_new_ip_range(
        self,
        hosting_provider: Hostingprovider,
        sample_hoster_user: User,
        green_ip: GreencheckIp,
    ):

        hosting_provider.save()
        sample_hoster_user.hostingprovider = hosting_provider
        sample_hoster_user.save()
        GreencheckIp.objects.count() == 1

        rf = APIRequestFactory()
        url_path = reverse("ip-range-list")

        sample_json = {
            "hostingprovider": hosting_provider.id,
            "ip_start": "192.168.178.121",
            "ip_end": "192.168.178.129",
        }

        request = rf.post(url_path, sample_json)
        request.user = sample_hoster_user

        view = IPRangeViewSet.as_view({"post": "create"})

        response = view(request)

        assert response.status_code == 201
        GreencheckIp.objects.count() == 2

        assert response.data["ip_start"] == "192.168.178.121"
        assert response.data["ip_end"] == "192.168.178.129"
        assert response.data["hostingprovider"] == hosting_provider.id

    @pytest.mark.skip(reason="Pending. ")
    def test_skip_duplicate_ip_range(
        self,
        hosting_provider: Hostingprovider,
        sample_hoster_user: User,
        green_ip: GreencheckIp,
    ):
        """
        When a user creates an IP Range, we want to avoid the case of them
        making a duplicate. IP Range. Even if we check in the serialiser
        class, we should make sure a sensible API error message is returned
        """
        pass