from django.urls import path
from . import views

app_name='api'
urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('logout/',views.LogoutView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('password/reset/confirm/<uidb64>/<token>/', views.PasswordResetConfirmAPIView.as_view(),
         name='password_reset_confirm'),

    path('regions/<int:country_id>/', views.RegionListView.as_view()),
    path('countries/', views.CountryListView.as_view()),
    path('my-books/<status>/',views.BookListCreateView.as_view()),
    path('my-books/<str:status>/<int:pk>/',views.BookDetailView.as_view()),
    path('all-books/',views.AllBookListView.as_view()),
    path('home/',views.HomeView.as_view())
]
