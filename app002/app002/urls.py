from wine import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('winenara_search', views.winenara_search),
    path('wine21_search',views.wine21_search),
    path('label_search',views.label_search)
]
