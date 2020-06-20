from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render

from base_app.views import BaseDeleteView, AjaxableResponseMixin, BaseEditView, BaseCreateView, BaseListView
from .forms import NetworkDetailForm
from .models import NetworkDetails
# Create your views here.


class NetworkDetailCreateView(BaseCreateView):
    model = NetworkDetails
    form_class = NetworkDetailForm
    template_name = 'network_details/create_network_detail.html'
    success_url = '/network_details'


class NetworkDetailEditView(BaseEditView):
    form_class = NetworkDetailForm
    template_name = 'network_details/create_network_detail.html'
    success_url = '/network_details'
    model = NetworkDetails


class NetworkDetailListView(BaseListView):
    model = NetworkDetails
    template_name = 'network_details/network_lists_detail.html'
    success_url = '/network_details'

    def get_queryset(self):
        queryset = super(NetworkDetailListView, self).get_queryset()
        try:
           queryset = NetworkDetails.objects.all()

        except ObjectDoesNotExist:
            pass

        return queryset.order_by('mac_address').filter(is_deleted=False)

    def get_context_data(self, **kwargs):
        context = {

            'title': "Network Details",
            'panel_title': 'Local Networks',
            'details': self.get_queryset(),
        }
        return context

    # def get_queryset(self):
    #     queryset = super(NetworkDetailListView, self).get_queryset()
    #     if self.request.GET.get('q'):
    #         query_text = self.request.GET.get('q')
    #         print(queryset,"--------")
    #         return queryset.filter(
    #             Q(auto_id__icontains=query_text) |
    #             Q(loop_back__icontains=query_text) |
    #             Q(host_name__icontains=query_text) |
    #             Q(mac_address__icontains=query_text)  |
    #             Q(sap_id__icontains=query_text)).select_related('mac_address').only('pk', 'auto_id')
    #     else:
    #         return queryset.select_related('mac_address').only('pk', 'auto_id', 'sap_id', 'mac_address', 'loop_back', 'host_name')


class NetworkDetailDeleteView(BaseDeleteView):
    model = NetworkDetails