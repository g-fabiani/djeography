from django.urls import path
from .views import (EntityListView, EntityDetailView,
                    EntityPublishView, EntityUnpublishView,
                    GeoJSONLayerByCategoryView, MapView, PopupView)
from django.views.generic import ListView
from . models import Address, Category

urlpatterns = [
    path('data/<slug:slug>.geojson', GeoJSONLayerByCategoryView.as_view(), name='data'),
    path('popup/<int:pk>/', PopupView.as_view(), name='popup'),
    path('fullscreen/', MapView.as_view(), name="map_fullscreen"),
    path('entities/', EntityListView.as_view(), name='list'),
    path('entities/<int:pk>/', EntityDetailView.as_view(), name='detail'),
    path('entities/<int:pk>/publish/', EntityPublishView.as_view(), name='publish'),
    path('entities/<int:pk>/unpublish/', EntityUnpublishView.as_view(), name='unpublish'),
]