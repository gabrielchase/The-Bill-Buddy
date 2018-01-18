from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from rest_framework.test import APIRequestFactory

from bills.models import Bill
from bills.tests.fixtures import (new_bill_info, new_bill, other_bill)
from bills.views import BillViewSet
from bills.utils import handle_service_instance

from users.tests.fixtures import (new_user, other_user)
from users.tests.utils import get_jwt_header

from random import randint

import json
import pytest

pytestmark = pytest.mark.django_db
User = get_user_model()
factory = APIRequestFactory()
BILLS_URI = 'api/bills/'


class TestBillsViews: 

    def test_bill_post(self, new_bill_info, new_user):
        view = BillViewSet.as_view({'post': 'create'})
        request = factory.post(
            BILLS_URI, 
            data=json.dumps(new_bill_info), 
            HTTP_AUTHORIZATION=get_jwt_header(new_user.email),
            content_type='application/json'
        )
        response = view(request)

        assert response.status_code == 201
        
        assert response.data.get('id')
        assert response.data.get('name') == new_bill_info['name']
        assert response.data.get('description') == new_bill_info['description']
        assert response.data.get('due_date') == new_bill_info['due_date']
        
        assert response.data.get('service', {}).get('id')
        assert response.data.get('service', {}).get('name') == new_bill_info['service']['name'].title()

        assert response.data.get('user_details', {}).get('id') == new_user.id
        assert response.data.get('user_details', {}).get('email') == new_user.email
        assert response.data.get('user_details', {}).get('username') == new_user.username
        assert response.data.get('user_details', {}).get('first_name') == new_user.first_name
        assert response.data.get('user_details', {}).get('last_name') == new_user.last_name

    def test_get_and_retrieve_own_bills(self, new_user, other_user): 
        Bill.objects.create(
            name=mixer.faker.first_name(),
            description=mixer.faker.text(),
            due_date=randint(1, 31),
            service=handle_service_instance(mixer.faker.genre()),
            user=new_user
        )
        
        Bill.objects.create(
            name=mixer.faker.first_name(),
            description=mixer.faker.text(),
            due_date=randint(1, 31),
            service=handle_service_instance(mixer.faker.genre()),
            user=new_user
        )

        good_list_view = BillViewSet.as_view({'get': 'list'})
        good_list_request = factory.get(
            BILLS_URI, 
            HTTP_AUTHORIZATION=get_jwt_header(new_user.email),
        )
        good_list_response = good_list_view(good_list_request)
        
        assert good_list_response.status_code == 200
        
        bills = good_list_response.data
        assert len(bills) == 2
        
        for bill in bills:
            assert bill.get('id')
            assert bill.get('user_details', {}).get('id') == new_user.id
            assert bill.get('user_details', {}).get('email') == new_user.email
            
            good_retrieve_view = BillViewSet.as_view({'get': 'retrieve'})
            good_retrieve_request = factory.get(
                BILLS_URI,
                HTTP_AUTHORIZATION=get_jwt_header(new_user.email),
            )
            good_retrieve_response = good_retrieve_view(good_retrieve_request, pk=bill.get('id'))
            
            assert good_retrieve_response.status_code == 200

    def test_get_other_bills_should_be_forbidden(self, new_user, other_user):
        b1 = Bill.objects.create(
            name=mixer.faker.first_name(),
            description=mixer.faker.text(),
            due_date=randint(1, 31),
            service=handle_service_instance(mixer.faker.genre()),
            user=new_user
        )

        assert b1.id
        assert b1.user == new_user

        bad_retrieve_view = BillViewSet.as_view({'get': 'retrieve'})
        bad_retrieve_request = factory.get(
            BILLS_URI,
            HTTP_AUTHORIZATION=get_jwt_header(other_user.email),
        )
        bad_retrieve_response = bad_retrieve_view(bad_retrieve_request, pk=b1.id)
        
        assert bad_retrieve_response.status_code == 403
