from rest_framework import serializers

from donations.models import Donation


class DonationSerializer(serializers.ModelSerializer):
    partial = True
    class Meta:
        model = Donation
        fields = ('id', 'is_taken',)