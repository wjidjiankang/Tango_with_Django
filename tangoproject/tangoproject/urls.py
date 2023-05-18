"""tangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,re_path,include
from rango import views
# from django.conf.urls import url


# from django.contrib import admin
# from django.urls import path,re_path,include
# from stock import views,dbtest,models
# from stock import login
# from django.conf.urls import url
from registration.backends.simple.views import RegistrationView

class MyRegisrationView(RegistrationView):
    def get_success_url(self,user):
        return '/rango/'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('rango/',include('rango.urls',namespace = 'rango')),
    path('accounts/',include('registration.backends.simple.urls')),
    path('accounts/register',MyRegisrationView.as_view(),name='registration_register')
]
