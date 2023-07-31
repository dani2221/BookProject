"""
URL configuration for BookProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from books.views import index, register, detail_view, cart, checkout_view, order_list_view
from django.contrib.auth import views as auth_views

from BookProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('book/<str:title>', detail_view, name='details'),
    path('register/', register, name='register'),
    path('cart/', cart, name='cart'),
    path('orders/', order_list_view, name='orders'),
    path('payment/', checkout_view, name='payment'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
