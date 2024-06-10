from django.urls import path
from .views import UserRegistrationView, VerifyOTP, RetryOTP, LoginUser, UserPoints, FeedbackApi, ForgetPass, Terminate

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', LoginUser.as_view(), name='user-login'),
    path('allusers/', UserRegistrationView.as_view(), name='allusers'),
    path('userupdate/<int:pk>', UserRegistrationView.as_view(), name='user-update'),
    path('userdelete/<int:pk>', UserRegistrationView.as_view(), name='user-delete'),
    path('verify/', VerifyOTP.as_view(), name='user-verify'),
    path('retry-otp/', RetryOTP.as_view(), name='retry-verify'),
    path('user-add-points/<int:pk>', UserPoints.as_view(), name='user-add-points'),
    path('feedback/', FeedbackApi.as_view(), name='feedback'),
    path('forget-password/', ForgetPass.as_view(), name='forget-password'),
    path('terminate/<int:pk>', Terminate.as_view(), name='terminate'),

]
