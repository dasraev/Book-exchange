from rest_framework import response, permissions, generics, parsers, status, mixins
from rest_framework.views import APIView
from . import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.db.models import Q
from user.models import Region, Country
from book.models import Book
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.reverse import reverse
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import ValidationError
from user.tasks import send_password_reset_email

User = get_user_model()

                        ################# USER ###########################
class RegisterView(generics.GenericAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(ObtainAuthToken):
    serializer_class = serializers.LoginSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        Token.objects.get(user=request.user).delete()
        return response.Response()


class PasswordResetView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = reverse('api:password_reset_confirm', kwargs={"uidb64": uidb64, "token": token},
                                request=request)
            subject = 'Password reset request'
            message = f'Hi {user.email},\n\nPlease click the link below to reset your password:\n{reset_url}'
            # to_email = [email]
            send_password_reset_email.delay(subject, message, email)
        return Response(status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(generics.GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            password = serializer.validated_data['password1']
            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (parsers.MultiPartParser,)

    def get_object(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id is None:
            return self.request.user
        try:
            return get_object_or_404(User, id=user_id)
        except Exception as e:
            raise ValidationError(e)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description="Enter user_id or just leave it blank",
                type=openapi.TYPE_STRING,
            )])
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description="Enter user_id or just leave it blank",
                type=openapi.TYPE_STRING)])
    def put(self, request, *args, **kwargs):
        if request.user != self.get_object():
            return Response(status=status.HTTP_403_FORBIDDEN)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, context={'user': user, 'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegionListView(generics.ListAPIView):
    serializer_class = serializers.RegionSerializer

    def get_queryset(self):
        return Region.objects.filter(country_id=self.kwargs['country_id'])


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = serializers.CountrySerializer


                ######################## BOOK ##################################

class BookListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.BookSerializer
    pagination_class = PageNumberPagination
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        if self.kwargs['status'].lower() not in ['wish', 'offer']:
            raise ValidationError('status should be wish or offer')
        if self.kwargs['status'].lower() == 'offer':
            books = Book.objects.filter(owner=self.request.user, status='O').select_related('owner').order_by('-date')
        elif self.kwargs['status'].lower() == 'wish':
            books = Book.objects.filter(owner=self.request.user, status='W').select_related('owner').order_by('-date')
        return books

    def get(self, request, *args, **kwargs):
        self.pagination_class.page_size = 10
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if kwargs['status'] not in ['offer', 'wish']:
            raise ValidationError('status should be wish or offer')
        if kwargs['status'] == 'offer':
            serializer.save(owner=request.user, status='O')
        elif kwargs['status'] == 'wish':
            serializer.save(owner=request.user, status='W')

        return Response(serializer.data)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BookDetailSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        if self.kwargs['status'] not in ['offer', 'wish']:
            raise ValidationError('status should be wish or offer')
        if self.kwargs['status'] == 'offer':
            book = get_object_or_404(Book, pk=self.kwargs['pk'], status='O')
        elif self.kwargs['status'] == 'wish':
            book = get_object_or_404(Book, pk=self.kwargs['pk'], status='W')
        return book

    def update(self, request, *args, **kwargs):
        if self.request.user != self.get_object().owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if self.request.user != self.get_object().owner:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


class HomeView(generics.ListAPIView, generics.GenericAPIView):
    serializer_class = serializers.BookSerializer
    pagination_class = PageNumberPagination
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        self.wished_books = Book.objects.filter(owner=self.request.user, status='W', active=True)
        offered_books = Book.objects.filter(status='O', active=True).select_related('owner')
        titles_list = list(self.wished_books.values_list('title', flat=True))
        queries = [Q(title__trigram_similar=title) for title in titles_list]  # create a list of Q objects
        combined_query = queries.pop() if queries else Q()  # pop the first Q object from the list, or create an empty Q object if the list is empty
        for query in queries:
            combined_query |= query
        matched_books = offered_books.filter(combined_query).order_by('-date')
        return matched_books

    def get(self, request, *args, **kwargs):
        self.pagination_class.page_size = 10
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return paginator.get_paginated_response({'wished_books': bool(self.wished_books), 'books': serializer.data})


class AllBookListView(generics.ListAPIView):
    model = Book
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        if self.request.query_params.get('status'):
            if self.request.query_params.get('status').lower() == 'wish':
                books = Book.objects.filter(status='W').select_related('owner').order_by('-date')
            elif self.request.query_params.get('status').lower() == 'offer':
                books = Book.objects.filter(status='O').select_related('owner').order_by('-date')
            else:
                raise ValidationError('status should be wish or offer')

        else:
            books = Book.objects.all().select_related('owner').order_by('-date')
        return books

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY,
                              description='Enter status or just leave it blank to see all books',
                              type=openapi.TYPE_STRING),

        ]
    )
    def get(self, request, *args, **kwargs):
        books = self.get_queryset()
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
