from django.urls import path
from .views import*
from django.contrib.auth import views
from .forms import*
urlpatterns = [
    path('login',AdminLoginView.as_view(),name='login'),
    path('logout',AdminLogoutView.as_view(),name='logout'),
    path('resetpassword/',views.PasswordResetView.as_view(template_name='resetpassword.html',form_class=MypasswordResetform), name='resetpassword'),
    path('resetpassword/done/',views.PasswordResetDoneView.as_view(template_name='resetpassword_done.html'), name='password_reset_done'),
    path('resetpasswordconfirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(template_name='resetpassword_confirm.html',form_class=MySetPasswordform), name='password_reset_confirm'),
    path('resetpasswordcomplete/',views.PasswordResetCompleteView.as_view(template_name='completeresetpassword.html'), name='password_reset_complete'),
    path('userRegistration',UserRegistration.as_view(),name='userRegistration'),
    path('userview',UserViews.as_view(),name='userview'),
    path('userdelete/<int:pk>/',UserDelete.as_view(),name='userdelete'),
    path('useredit/<int:pk>/',UserEditView.as_view(),name='useredit'),
  
]