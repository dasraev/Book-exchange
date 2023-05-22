from django.urls import path
from .views import *

urlpatterns = [
    path('offer/', OfferCreateView.as_view(), name='offer'),
    path('offer/<int:pk>/', OfferEditView.as_view(), name='offer-edit'),
    path('wish/', WishCreateView.as_view(), name='wish'),
    path('wish/<int:pk>/', WishEditView.as_view(), name='wish-edit'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('all/', AllBookListView.as_view(), name='all-books'),
    path('wishlist/', BookListView.as_view(), name='wishlist'),
    path('offerlist/', BookListView.as_view(), name='offerlist')
]
