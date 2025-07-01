from rest_framework import serializers
from .models import BloodRequest
from django.utils.timesince import timesince
from django.utils.timezone import now
from .models import Donor
from django.contrib.auth import authenticate

class BloodRequestSerializer(serializers.ModelSerializer):
    requestedAt = serializers.SerializerMethodField()

    class Meta:
        model = BloodRequest
        fields = [
            'id',
            'name',
            'bloodGroup',
            'contact',
            'location',
            'hospital',
            'patientAge',
            'unitsNeeded',
            'urgency',
            'requiredBy',
            'notes',
            'requestedAt',   # camelCase for frontend compatibility
            'status',
        ]

    def get_requestedAt(self, obj):
        delta = timesince(obj.requestedAt, now())
        if 'minute' in delta or 'hour' in delta:
            return f"{delta.split(',')[0]} ago"
        return "just now"





class DonorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Donor
        fields = '__all__'
        read_only_fields = ['id', 'is_staff', 'is_active', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        donor = Donor(**validated_data)
        donor.set_password(password)
        donor.save()
        return donor

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class DonorLoginSerializer(serializers.Serializer):
    contact = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        contact = data.get('contact')
        password = data.get('password')

        try:
            user = Donor.objects.get(contact=contact)
        except Donor.DoesNotExist:
            raise serializers.ValidationError("Donor not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password")

        data['user'] = user
        return data