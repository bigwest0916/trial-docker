from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # 一覧画面
    path('', views.QestionVersionList.as_view(), name='index'),
    path('', views.QestionList.as_view(), name='index'),
]
