
from rest_framework.serializers import ModelSerializer
from express.models import ParcelPickup, Park, Partner,Parcel
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



class RegisterSerializer(ModelSerializer):
    """USER REGISTERATION SERIALIZER"""
    password = serializers.CharField(max_length=68,min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email']
    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ParcelPickupSerializer(ModelSerializer):
    """PARCEL PICKUP SERIALIZER"""
    class Meta:
        model = ParcelPickup
        fields = '__all__'

class PatnerSerializer(ModelSerializer):
    """PARTNER SERIALIZER"""
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Partner
        fields = '__all__'

class ParkSerializer(ModelSerializer):
    """PARK SERIALIZER"""
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Park
        fields= '__all__'

class UserSerializer(ModelSerializer):
    """USER MODEL SERIALIZERS"""
    creator = PatnerSerializer(many=True)
    owner = ParkSerializer(many=True)
    class Meta:
        model = User
        fields = ['id','username','creator','owner']


class ParcelSerializer(ModelSerializer):
    """PARCEL SERIALIZER"""
    parcel = ParcelPickupSerializer(read_only=True)
    current_location = ParkSerializer(read_only=True)
    class Meta:
        model = Parcel
        fields = ['tracking_id','riders_contact','parcel_status','parcel','current_location']

