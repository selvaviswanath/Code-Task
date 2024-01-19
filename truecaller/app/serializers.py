from rest_framework import serializers
from .models import GlobalContact, User, Contact

class GlobalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalContact
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'