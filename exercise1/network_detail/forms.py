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

    def clean_mac_address(self):
        """Method to clean the mac_address name.

            Here we check if the entered Mac Address is valid or not.

        :return: cleaned_data, used in the views to further perform any validation and later
        used by save method.
        :rtype: dictionary
        """
        # Calling clean() method of super class
        cleaned_data = super(NetworkDetailForm, self).clean()
        if "first_name" in cleaned_data.keys():
            if cleaned_data['mac_address'].isalpha():
                cleaned_data['mac_address'] = str(cleaned_data['mac_address'])
            else:
                raise forms.ValidationError("mac_address should not contain special characters or numbers.")
        return cleaned_data['mac_address']

    def save(self, commit=True):
        """Method overridden to abstract network details creation .

            This method is overridden to abstract the creation of a new record
            when a network detail object is created.

        :param commit: used to assert whether to commit to DB right away of merely instantiate the object.
        :type boolean:
        :return: NetworkDetail object that has all the required values.
        :rtype: NetworkDetails
        """
        # data = super(NetworkDetailForm, self).save(commit=False)
        # Calling clean() method of super class
        cleaned_data = super(NetworkDetailForm, self).clean()
        print(cleaned_data,"-------------")
        if commit:
            cleaned_data.save()
        return cleaned_data
