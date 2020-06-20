from django.db.models import Q
from django.shortcuts import render

from base_app.views import BaseDeleteView, AjaxableResponseMixin, BaseEditView, BaseCreateView, BaseListView
from .forms import NetworkDetailForm
from .models import NetworkDetails
# Create your views here.


class NetworkDetailCreateView(BaseCreateView):
    form_class = NetworkDetailForm
    template_name = 'network_details/create_network_detail.html'
    success_url = '/network_details'
    model = NetworkDetails


class NetworkDetailEditView(BaseEditView):
    form_class = NetworkDetailForm
    template_name = 'network_details/create_network_detail.html'
    success_url = '/network_details'
    model = NetworkDetails


class NetworkDetailListView(BaseListView):
    model = NetworkDetails
    template_name = 'network_details/network_details.html'

    def get_queryset(self):
        queryset = super(NetworkDetailListView, self).get_queryset()
        return queryset
        # if self.request.GET.get('q'):
        #     query_text = self.request.GET.get('q')
        #     return queryset.filter(
        #         Q(auto_id__icontains=query_text) | Q(loop_back__icontains=query_text) | Q(
        #             host_name__icontains=query_text) | Q(
        #             mac_address__icontains=query_text) | Q(phone__icontains=query_text) | Q(
        #             sap_id__icontains=query_text)).select_related('user').only('pk', 'auto_id', 'user__username', 'first_name', 'last_name', 'email', 'phone', 'department')
        # else:
        #     return queryset.select_related('user').only('pk', 'auto_id', 'first_name', 'user__username', 'last_name', 'email', 'phone', 'department', 'user__is_active')


class NetworkDetailDeleteView(BaseDeleteView):
    model = NetworkDetails