from rest_framework import serializers
from .models import User, Farm, Cow, Activity, MilkProduction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'farm']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        role = data.get('role')
        farm = data.get('farm')
        if role == 'farmer':
            if not farm:
                raise serializers.ValidationError("Farmer must be assigned to a farm.")
            if farm.farmers.exists():
                raise serializers.ValidationError("A farm can only have one farmer.")
        elif role in ['superadmin', 'agent'] and farm:
            raise serializers.ValidationError("Only farmers can be assigned to a farm.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'

    def validate_agent(self, value):
        if value.role != 'agent':
            raise serializers.ValidationError("Agent must have role 'agent'.")
        return value

class CowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cow
        fields = '__all__'

    def validate_owner(self, value):
        if value.role != 'farmer':
            raise serializers.ValidationError("Owner must be a farmer.")
        return value

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class MilkProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MilkProduction
        fields = '__all__'