"""Forms related to staff creation and management.

    This module contains all the Django Forms that are responsible for creating
    and managing the Staff instance in the project. Primary operations on Staff
    objects are:
        1. Create new Staff instance.
        2. Edit Staff details such as name, phone, email etc.
        3. Change Staff's user password.

    Each of these operations are split into separate forms as the fields are slightly
    different.
"""
from django import forms
from django.forms import TextInput
from .models import NetworkDetails
from django.utils.translation import ugettext_lazy as _


class NetworkDetailForm(forms.ModelForm):
    """Form used to create a Network Detail instance.

        This Form allows the creation of new Network Detail objects. And additional
        fields to enable network creation, such as loopback,sap_id.

    """

    class Meta:
        model = NetworkDetails
        exclude = ['creator', 'updater', 'date_added', 'date_updated', 'auto_id', 'is_deleted']
        widgets = {
            'sap_id': TextInput(
                attrs={'class': 'required form-control col-md-7 col-xs-12', 'placeholder': 'Sap Id'}),
            'loop_back': TextInput(
                attrs={'class': 'form-control col-md-7 col-xs-12', 'placeholder': 'Loopback'}),
            'mac_address': TextInput(
                attrs={'class': 'form-control col-md-7 col-xs-12', 'placeholder': 'Mac Address'}),
            'host_name': TextInput(
                attrs={'class': 'form-control col-md-7 col-xs-12', 'placeholder': 'Host name'}),
        }
        error_messages = {
            'loop_back': {
                'required': _("Loop Back field is required."),
            },
            'host_name': {
                'required': _("Host Name field is required."),
            },
            'mac_address': {
                'required': _("Mac Address field is required."),
            },
            'sap_id': {
                'required': _("SAP Id field is required."),
            },

        }

    def save(self, commit=True):
        """Method overridden to abstract user creation when creating staff.

            This method is overridden to abstract the creation of a new User
            when a Staff object is created. Thus the developer is not required
            to create a separate User instance and add a relationship to the
            new Staff object. This also avoids the possibility of incorrect usage
            of the staff model.

        :param commit: used to assert whether to commit to DB right away of merely instantiate the object.
        :type boolean:
        :return: Staff object that has all the required values.
        :rtype: Staff
        """
        data = super(StaffForm, self).save(commit=False)

        user = User.objects.create_user(username=data.email.split('@')[0],
                                        email=data.email,
                                        password=self.cleaned_data['password_1'])
        data.user = user
        if commit:
            data.save()
        return data
