from django.contrib.auth.models import User
from rest_framework import serializers

from donations.models import Donation


class DonationSerializer(serializers.ModelSerializer):
    partial = True

    class Meta:
        model = Donation
        fields = ('id', 'is_taken',)


class UserProfileSerializer(serializers.ModelSerializer):
    partial = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class UserPasswordSerializer(serializers.Serializer):
    partial = True
    model = User
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
