from django.urls import path, include
from .views import RegisterView, UserList, UserDetail, UserDetailHighlight
from rest_framework import routers

router = routers.DefaultRouter()
router.register('register', RegisterView, 'list')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
    path('users/<int:pk>/', UserDetailHighlight.as_view(), name='user-highlight'),
]
