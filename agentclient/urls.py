from rest_framework import routers
from django.urls import path, include
# from . import views

router = routers.DefaultRouter()
# router.register(r'query', views.QueryViewSet, basename='query')

urlpatterns = [
    path('', include(router.urls)),
    ]

# # Added by Sigmus
# from django.urls import path
# from .views import process_contact

# urlpatterns = [
#     path("process_contact/", process_contact, name="process_contact"),
# ]
