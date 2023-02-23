from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username']

class ProfileSerializer(serializers.ModelSerializer):

    # use print(repr(serializer)) in shell to see how it's serialized
    user = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = Profile
        fields = ['user', 'username', 'email', 'number', 'gender', 'dob', 'variables', 'data']

    '''
    manual implementation (what ModelSerializer does)
    # add user & variables later (skipping now because have to use Model.Serializer)

    #user = serializers.OneToOneField(primary_key=True)
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    number = serializers.CharField(max_length=11)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES, default='Woman')
    dob = serializers.DateField()
    #variables = serializers.ManyToManyField(Variable, related_name="users")
    data = serializers.JSONField(default=dict)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """

        return instance
        '''
    
