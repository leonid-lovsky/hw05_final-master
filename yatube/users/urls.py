from django.urls import path

from . import views as users_views

app_name = 'users'

urlpatterns = [
    path('signup/',
         users_views.MyUserCreationView.as_view(),
         name='signup'),

    path('login/',
         users_views.MyLoginView.as_view(),
         name='login'),

    path('logout/',
         users_views.MyLogoutView.as_view(),
         name='logout'),

    path('password_change/',
         users_views.MyPasswordChangeView.as_view(),
         name='password_change'),

    path('password_change/done/',
         users_views.MyPasswordChangeDoneView.as_view(),
         name='password_change_done'),

    path('password_reset/',
         users_views.MyPasswordResetView.as_view(),
         name='password_reset'),

    path('password_reset/done/',
         users_views.MyPasswordResetDoneView.as_view(),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         users_views.MyPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    path('reset/done/',
         users_views.MyPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
