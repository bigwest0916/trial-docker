from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # 一覧画面
    path('', views.index, name='index'),
    path('create/<int:diagnosis_id>/', views.create, name='hs'),
    path('change/<int:diagnosis_id>/', views.change, name='hs'),
]
