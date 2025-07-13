from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('sign-up/' , views.SignUpView.as_view(), name='sign_up_page'),
    path('log-in/' , views.LogInView.as_view(), name='log_in_page'),
    path('log-out/' , LogoutView.as_view(next_page="first_page"), name='logout'),
    path('forgot-password/' , views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('verify-page/' , views.VerifyCodeView.as_view(), name='verify_page'),
    path('reset-password/' , views.ResetPasswordView.as_view(), name='reset_password_page'),
    path('signup-verify/' , views.SignUpVerifyCode.as_view(), name='signup_verify_page'),
    path('user-panel/' , views.UserPanelView.as_view(), name='user_panel_page'),
    # path('subscribe-page/' , views.SubscribeView.as_view(), name='subscribe_page')
]