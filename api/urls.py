from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'matches', views.MatchViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
