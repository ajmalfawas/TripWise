from rest_framework import serializers
from django.contrib.auth.models import User
from tripmaster.models import Tripdb

class userserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class tripSerializers(serializers.ModelSerializer):
    class Meta:
        model=Tripdb
        fields = '__all__'
        read_only_fields = ['created_by']

    

