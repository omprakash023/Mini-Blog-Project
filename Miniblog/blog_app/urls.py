from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    HandleLogin,
    HandleLogout,
    HandleRegister,
    ShowAllBlogs,
    UserBlogs,


)

urlpatterns = [
    path('',ShowAllBlogs.as_view(),name='index'),
    path('register/',HandleRegister.as_view(),name='register'),
    path('login/',HandleLogin.as_view(),name='login'),
    path('logout/',HandleLogout.as_view(),name='logout'),
    path('userblog/',UserBlogs.as_view(),name='userblog'),
    path('userblog/<int:blog_id>',UserBlogs.as_view(),name='userblog'),
    # path('logout/',HandleLogout.as_view(),name='logout'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]