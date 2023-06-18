from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calcul_totaux/', views.calcul_totaux, name='calcul_totaux'),
    path('prediction/', views.call_model.as_view(), name='prediction'),
    path('pred_list/', views.pred_list, name='pred_list'),
    path('list_manuel/', views.list_manuel, name='list_manuel'),
    path('pickday/', views.pick_day, name='pickday'),
    path('showprediction/', views.show_pred, name='show_pred'),
    path('storepred/', views.store_pred, name='store_pred'),
    path('store_manuel/', views.store_manuel, name='store_manuel'),
    path('list_monit/', views.list_monit, name='list_monit'),
]
