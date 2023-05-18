# from django.contrib import admin
from django.urls import path,re_path,include
from rango import views
# from django.conf.urls import url

app_name = 'rango'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.index, name='index'),
    # path('rango/',include('rango.urls',namespace = 'rango')),
    re_path(r'^$', views.index, name='index'),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category, name='show_category'),
    re_path(r'^add_category/$', views.add_category, name='add_category'),
    # re_path(r'^add_page/(?P<category_name_slug>[\w\-]+)/$', views.add_page, name='add_page'),
    # re_path(r'^(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    # path('add_page',views.add_page),
    re_path(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
    path('about/',views.about,name='about'),
    # path('register/', views.register, name='register'),
    # path('login/',views.user_login, name='login'),
    # path('restricted/', views.restricted, name='restricted'),
    # path('logout/', views.user_logout, name='logout'),
    path('like/', views.like_category, name='like_category'),
    path('suggest/',views.suggest_category, name='suggest_category'),
]
