from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from user.models import Region, Country
from book.models import Book, CONDITION, STATUS
import re
from rest_framework.validators import UniqueValidator

User = get_user_model()


def validate_password_complexity(password):
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search('[A-Z]', password):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search('[a-z]', password):
        raise serializers.ValidationError("Password must contain at least one lowercase letter.")
    if not re.search('[0-9]', password):
        raise serializers.ValidationError("Password must contain at least one digit.")


class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all())
    education = serializers.CharField(max_length=100)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already taken')
        return value

    def validate(self, attrs):

        if attrs['region'] not in attrs['country'].regions.all():
            raise serializers.ValidationError('the region is not part of the country')
        return attrs

        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        validate_password_complexity(attrs['password1'])

    def create(self, validated_data):
        return User.objects.create_user(email=validated_data['email'],
                                        country=validated_data['country'],
                                        region=validated_data['region'],
                                        education=validated_data['education'],
                                        password=validated_data['password1']
                                        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=128)
    password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password_complexity(data['password1'])
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, validators=[UniqueValidator(User.objects.all())])

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'country', 'region', 'education', 'profile_pic', 'gender',
                  'age', ]


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['country'] = {"id": instance.country.id, "name": instance.country.name}
        rep['region'] = {"id": instance.region.id, "name": instance.region.name}
        return rep

    def validate_region(self, value):
        print(9012312,self.context['user'])
        if value not in self.context['user'].country.regions.all():
            raise serializers.ValidationError('the region is not part of the country')
        return value

    def validate(self, attrs):
        print(2222,attrs)
        if attrs.get('region') and attrs.get('country') and attrs.get('region') not in attrs.get(
                'country').regions.all():
            raise serializers.ValidationError('the region is not part of the country')
        return attrs



class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=50)
    owner = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(choices=STATUS, read_only=True)
    condition = serializers.ChoiceField(choices=CONDITION, required=False, default='G')
    cover = serializers.ImageField(required=False)
    active = serializers.BooleanField(required=False, default=True)
    date = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book


class BookDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100, required=False)
    author = serializers.CharField(max_length=50, required=False)
    owner = serializers.CharField(read_only=True)
    cover = serializers.ImageField(required=False)
    active = serializers.BooleanField(required=False, default=True)
    status = serializers.ChoiceField(choices=STATUS, read_only=True)
    condition = serializers.ChoiceField(choices=CONDITION, required=False)
    date = serializers.DateTimeField(read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.cover = validated_data.get('cover', instance.cover)
        instance.active = validated_data.get('active', instance.active)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.save()
        return instance


class RegionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, read_only=True)


class CountrySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100, read_only=True)

