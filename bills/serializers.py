from django.contrib.auth import get_user_model

from rest_framework import serializers

from bills.models import (Bill, Service)

from users.serializers import (UserSerializer)

import json

User = get_user_model()


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'name',)


class BillSerializer(serializers.ModelSerializer):

    user_details = serializers.SerializerMethodField()
    service = ServiceSerializer()

    class Meta:
        model = Bill
        fields = ('id', 'name', 'description', 'due_date', 'service', 'user_details')

    def get_user_details(self, obj):
        user_details = {
            'id': obj.user.id,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email,
            'username': obj.user.username,
            'date_joined': obj.user.date_joined.isoformat(),
            'country': obj.user.details.country,
            'mobile_number': obj.user.details.mobile_number
        }

        return json.loads(json.dumps(user_details))

    def create(self, data):
        print('Creating a Bill with the following data: ', data)
        print('request.user: ', self.context['request'].user)

        service_instance = None
        service_name = data.get('service', {}).get('name').title()

        try:
            service_instance = Service.objects.get(name=service_name)
        except Service.DoesNotExist:
            service_instance = Service.objects.create(name=service_name)

        print('service_inst1ance: ', service_instance)
        
        due_date = data.get('due_date')
        
        if due_date:
            if due_date > 31 or due_date < 1:
                raise ValueError('Due date must be between 1 and 31')
            else:
                pass
        
        new_bill = Bill.objects.create(
            name=data.get('name'),
            description=data.get('description'),
            due_date=due_date,
            service=service_instance,
            user=self.context['request'].user
        )

        print('New bill created: ', new_bill)
        
        return new_bill
        