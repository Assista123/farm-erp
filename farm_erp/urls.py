from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect


def logout_view(request):
    auth_logout(request)
    return redirect('login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='core/login.html'), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', include('core.urls')),
]