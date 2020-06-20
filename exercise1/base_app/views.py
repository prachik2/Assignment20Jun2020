from django.shortcuts import render
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView, CreateView, ListView


# Create your views here.
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        print("Called")
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        response_data = {
            'status': 'false',
            'stable': 'true',
            'title': 'Form validation error',
            'message': "Invalid values"
        }
        if self.request.is_ajax():
            return JsonResponse(response_data, status=200)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        response_data = {
            'status': 'true',
            'title': 'Successfully {}'.format(self.action_message),
            'redirect': 'true',
            'redirect_url': self.success_url,
            'message': '{} {} successfully.'.format(form.instance.__class__.__name__, self.action_message),
        }
        if self.request.is_ajax():
            return JsonResponse(response_data)
        else:
            return response


class BaseCreateView(AjaxableResponseMixin, CreateView):
    action_message = 'created'

    def form_valid(self, form):
        print("form")
        form.instance.creator = self.request.user
        form.instance.updater = self.request.user

        return super(BaseCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(BaseCreateView, self).get_context_data(**kwargs)

        context.update({'title': self.form_class.Meta.model.__name__, 'redirect': True, 'panel_title': 'Create'})
        return context


class BaseEditView(AjaxableResponseMixin, UpdateView):
    context_object_name = 'instance'
    action_message = 'edited'

    def get_queryset(self):
        return self.model.objects.active().filter(pk=self.kwargs['pk'])

    def get(self, request, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        form.instance.updater = self.request.user
        return

    def get_context_data(self, **kwargs):
        context = super(BaseEditView, self).get_context_data(**kwargs)

        context.update({'title': self.model.__name__, 'redirect': True, 'panel_title': 'Edit: {}'.format(self.object)})
        return context


class BaseListView(ListView):
    context_object_name = 'instances'

    def get(self, request, *args, **kwargs):
        if request.GET.get('paginate_by'):
            self.paginate_by = request.GET.get('paginate_by')
        else:
            self.paginate_by = 100
        return super(BaseListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.GET.get('sort_by'):
            queryset = self.model.objects.active().order_by(self.request.GET.get('sort_by'))
        else:
            queryset = self.model.objects.active()
        return queryset

    def get_context_data(self, **kwargs):
        title = self.model.__name__
        if self.request.GET.get('q'):
            title += '-{}'.format(self.request.GET.get('q'))
        context = super(BaseListView, self).get_context_data(**kwargs)

        context.update({'title': title, 'panel_title': '{} List'.format(self.model.__name__)})
        return context


class BaseDeleteView(DetailView):
    context_object_name = 'instance'

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        referrer = request.META.get('HTTP_REFERER')
        if self.object:
            self.object.remove(updater=request.user)
            response_data = {
                'status': 'true',
                'title': 'Successfully Deleted',
                'redirect': 'true',
                'redirect_url': referrer,
                'message': '{}: {} successfully deleted.'.format(self.object.__class__.__name__, self.object),
            }
        else:
            response_data = {
                'status': 'false',
                'stable': 'true',
                'title': 'Error',
                'message': "Unable to delete this {}: {}".format(self.object.__class__.__name__, self.object)
            }

        return HttpResponse(json.dumps(response_data), content_type='application/javascript')
