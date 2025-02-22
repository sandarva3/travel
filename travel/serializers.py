from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'fullname', 'age', 'nationality', 'gender']
    
    def create(self, valid_data): # valid_data is dictionary object returned by .is_valid() method.
        user = CustomUser.objects.create_user( # we use django's create_user method to ensure that password is hashed while creating user instance.
            username = valid_data['username'],
            email = valid_data['email'],
            fullname = valid_data['fullname'],
            age = valid_data['age'],
            nationality = valid_data['nationality'],
            gender = valid_data['gender'],
        )
        return user