from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # 一覧画面
    path('', views.index, name='index'),
    path('diag/', views.diag, name='diag'),
    path('hs/<int:diagnosis_id>/', views.hs, name='hs'),

]
