from django.urls import path

from . import views

app_name = "network_detail"

urlpatterns = [
    path('network_details', views.NetworkDetailListView.as_view(), name='network_details'),
    path('create-network_details/', views.NetworkDetailCreateView.as_view(), name='create_network_details'),
    path('delete-network_details/<int:pk>', views.NetworkDetailDeleteView.as_view(), name='delete_network_details'),
    path('edit-network_details/<int:pk>', views.NetworkDetailEditView.as_view(), name='edit_network_details'),
]
