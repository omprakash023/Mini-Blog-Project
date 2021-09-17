from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import(
                   Index,
                   HandleLogin,
                   HandleLogout,
                   HandleRegister,
                 
                )


urlpatterns = [
    path('',Index.as_view(),name='index'),
    path('signup/',HandleRegister.as_view(),name='signup'),
    path('login/',HandleLogin.as_view(),name='login'),
    path('logout/',HandleLogout.as_view(),name='logout'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]